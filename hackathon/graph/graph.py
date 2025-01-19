from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph
from hackathon.graph.chains.router import question_router, RouteQuery
from hackathon.graph.consts import (
    EXTRACT_METADATA,
    KNOWLEDGE_ENRICHER,
    QUERY_MAKER,
    GENERATE,
    FORMAT_OUTPUT,
    GRADE_DOCUMENTS,
    RETRIEVE,
)

from hackathon.graph.nodes import knowledge_enricher
from hackathon.graph.nodes.extract_metadata import extract_metadata
from hackathon.graph.nodes.query_maker import query_maker
from hackathon.graph.nodes.generate import generate
from hackathon.graph.nodes.format_output import format_output
from hackathon.graph.nodes.grade_documents import grade_documents
from hackathon.graph.nodes.retrieve import retrieve

from hackathon.graph.state import GraphState
from hackathon.session import SessionManager


memory = MemorySaver()


workflow = StateGraph(GraphState)

workflow.add_node(EXTRACT_METADATA, extract_metadata)
workflow.add_node(KNOWLEDGE_ENRICHER, knowledge_enricher)
workflow.add_node(QUERY_MAKER, query_maker)
workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GENERATE, generate)
workflow.add_node(FORMAT_OUTPUT, format_output)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)

workflow.set_entry_point(EXTRACT_METADATA)

workflow.add_edge(EXTRACT_METADATA, QUERY_MAKER)
workflow.add_edge(QUERY_MAKER, RETRIEVE)
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_edge(GRADE_DOCUMENTS, GENERATE)
workflow.add_edge(GENERATE, FORMAT_OUTPUT)

app = workflow.compile(checkpointer=memory)

app.get_graph().draw_mermaid_png(output_file_path="graph.png")
