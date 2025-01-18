from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from hackathon.graph.chains.answer_grader import answer_grader
from hackathon.graph.chains.hallucination_grader import (
    hallucination_grader,
)
from hackathon.graph.chains.router import question_router, RouteQuery
from hackathon.graph.consts import (
    GENERATE,
    GRADE_DOCUMENTS,
    RETRIEVE,
    WEBSEARCH,
)
from hackathon.graph.nodes.retrieve import retrieve
from hackathon.graph.nodes.grade_documents import grade_documents
from hackathon.graph.nodes.generate import generate
from hackathon.graph.nodes.web_search import web_search

from hackathon.graph.state import GraphState

load_dotenv()
memory = MemorySaver()


def decide_to_generate(state):
    """Decides whether to generate an answer or not based
    on the quality of retrieved documents.
    """
    print("---ASSESS GRADED DOCUMENTS---")

    if state.web_search:
        print(
            "---DECISION: NOT ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, INCLUDE WEB SEARCH---"
        )
        return WEBSEARCH
    else:
        print("---DECISION: GENERATE---")
        return GENERATE


def grade_generation_grounded_in_documents_and_question(
    state: GraphState,
) -> str:
    """Grades the generation based on whether it is grounded in the documents and
    addresses the question.
    """
    print("---CHECK HALLUCINATIONS---")
    question = state.question
    documents = state.documents
    generation = state.generation

    hallucination_score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    )

    if hallucination_score.binary_score:
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        print("---GRADE GENERATION vs QUESTION---")
        answer_grader_score = answer_grader.invoke(
            {"question": question, "generation": generation}
        )
        if answer_grader_score.binary_score:
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    else:
        print("---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY---")
        return "hallucination"


def route_question(state: GraphState) -> str:
    print("---ROUTE QUESTION---")
    question = state.question
    source: RouteQuery = question_router.invoke({"question": question})  # type: ignore

    if source.datasource == WEBSEARCH:
        print("---ROUTE QUESTION TO WEB SEARCH---")
        return WEBSEARCH
    elif source.datasource == "vectorstore":
        print("---ROUTE QUESTION TO RAG---")
        return RETRIEVE


workflow = StateGraph(GraphState)
workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(WEBSEARCH, web_search)

workflow.set_conditional_entry_point(
    route_question,
    {
        WEBSEARCH: WEBSEARCH,
        RETRIEVE: RETRIEVE,
    },
)
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    {
        WEBSEARCH: WEBSEARCH,
        GENERATE: GENERATE,
    },
)
workflow.add_edge(WEBSEARCH, GENERATE)
workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_documents_and_question,
    {
        "hallucination": GENERATE,
        "useful": END,
        "not useful": WEBSEARCH,
    },
)


app = workflow.compile(checkpointer=memory)

app.get_graph().draw_mermaid_png(output_file_path="graph.png")
