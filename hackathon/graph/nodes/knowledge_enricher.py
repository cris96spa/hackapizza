from typing import Any, Dict
from hackathon.graph.state import GraphState
from hackathon.graph.chains.enricher_decision_maker import (
    galactic_code_chain,
    cooking_manual_chain,
    planet_distance_chain,
)
from hackathon.session import SessionManager

llm = 
def knowledge_enricher(state: GraphState) -> Dict[str, Any]:
    """
    Arricchisce la conoscenza del grafo con le informazioni aggiuntive estratte dalle knowledge base esterne.
    """
    question = state.question

    need_planet_distance = planet_distance_chain.invoke({"question": question})

    near_planets = []

    if need_planet_distance:
        near_planets = 

    return {
        "code_documents": galactic_documents,
        "manual_documents": manual_documents,
        "near_planets": near_planets,
    }
