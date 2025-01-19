from typing import Any, Dict

from hackathon.graph.chains.retrieval_grade import retrieval_grader
from hackathon.graph.state import GraphState
from hackathon.graph.models import GradeDocuments


def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the question
    If any document is not relevant, we will set a flag to run web search

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated web_search state
    """
    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state.question
    documents = state.documents

    filtered_docs = []

    for doc in documents:
        score: GradeDocuments = retrieval_grader.invoke(
            {"question": question, "document": doc}
        )  # type: ignore
        grade = score.binary_score

        if grade:
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(doc)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")

    return {"documents": filtered_docs}
