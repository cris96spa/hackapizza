from typing import Any, Dict
from hackathon.graph.models import PlanetDistanceResponse
from hackathon.graph.prompts import (
    COMPUTE_PLANET_DISTANCE_PROMPT,
    GALACTIC_CODE_PROMPT,
    COOKING_MANUAL_PROMPT,
    PLANET_DISTANCE_PROMPT,
)
from hackathon.graph.state import GraphState
from hackathon.graph.chains.enricher_decision_maker import (
    galactic_code_chain,
    cooking_manual_chain,
    planet_distance_chain,
)
from langchain_core.prompts import ChatPromptTemplate
from hackathon.graph.tools.planet_distance import planet_distance
from hackathon.session import SessionManager
from langchain_core.runnables import RunnableSequence
from hackathon.graph.models import KnowledgeEnrichmentResponse, Planet

llm = SessionManager().model_manager.model
llm.bind_tools([planet_distance])
llm_with_structured_output = llm.with_structured_output(PlanetDistanceResponse)


def knowledge_enricher(state: GraphState) -> Dict[str, Any]:
    """
    Arricchisce la conoscenza del grafo con le informazioni aggiuntive estratte dalle knowledge base esterne.
    """
    question = state.question
    llm = SessionManager().model_manager.model
    structured_llm_generator = llm.with_structured_output(KnowledgeEnrichmentResponse)

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

    near_planets = []

    if need_planet_distance:
        query_generation_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", COMPUTE_PLANET_DISTANCE_PROMPT),
                (
                    "human",
                    "Domanda dell'utente: {question}",
                ),
            ]
        )

        llm = SessionManager().model_manager.model
        llm.bind_tools([planet_distance])
        llm_with_structured_output = llm.with_structured_output(PlanetDistanceResponse)

        query_generator: RunnableSequence = (
            query_generation_prompt | llm_with_structured_output
        )  # type: ignore

        near_planets = query_generator.invoke({"question": question})

    return {
        "manual_documents": manual_documents,
        "code_documents": galactic_documents,
        "near_planets": near_planets.planets,
    }
