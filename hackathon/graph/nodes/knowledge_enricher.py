from typing import Any, Dict
from hackathon.graph.state import GraphState
from hackathon.graph.chains.enricher_decision_maker import (
    galactic_code_chain,
    cooking_manual_chain,
    planet_distance_chain,
)
from hackathon.session import SessionManager


def knowledge_enricher(state: GraphState) -> Dict[str, Any]:
    """
    Arricchisce la conoscenza del grafo con le informazioni aggiuntive estratte dalle knowledge base esterne.
    """
    question = state.question

    need_galactic_code = galactic_code_chain.invoke({"question": question})
    need_cooking_manual = cooking_manual_chain.invoke({"question": question})
    need_planet_distance = planet_distance_chain.invoke({"question": question})

    galactic_documents = []
    manual_documents = []
    near_planets = []
    retriever = SessionManager().vectorstore_manager.vectorstore.as_retriever(
        search_kwargs={"k": 5}
    )
    if need_galactic_code:
        galactic_documents = retriever.invoke(question, filter={"is_code": True})
    if need_cooking_manual:
        manual_documents = retriever.invoke(question, filter={"is_manual": True})
    if need_planet_distance:
        near_planets = retriever.invoke(question, filter={"is_planet": True})

    return {
        "code_documents": galactic_documents,
        "manual_documents": manual_documents,
        "near_planets": near_planets,
    }
