from typing import Any, Dict
from hackathon.graph.state import GraphState
from hackathon.session import SessionManager

retriever = SessionManager().vectorstore_manager.retriever


def retrieve(state: GraphState) -> Dict[str, Any]:
    """
    Retrieve documents from the vector store.

    Args:
        state: The current state of the graph.

    Returns:
        A dictionary containing the retrieved documents.
    """
    documents = retriever.invoke(state.question)
    return {"documents": documents}
