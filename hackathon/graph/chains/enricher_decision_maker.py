from langchain_core.runnables import RunnableSequence
from hackathon.session import SessionManager
from langchain.prompts import ChatPromptTemplate
from hackathon.graph.models import KnowledgeEnrichmentResponse, Planet
from hackathon.graph.prompts import (
    PLANET_DISTANCE_PROMPT,
    COOKING_MANUAL_PROMPT,
    GALACTIC_CODE_PROMPT,
)

llm = SessionManager().model_manager.model
structured_llm_generator = llm.with_structured_output(KnowledgeEnrichmentResponse)

galactic_code_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", GALACTIC_CODE_PROMPT),
        (
            "human",
            "Query dell'utente: \n\n {question}",
        ),
    ]
)
cooking_manual_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", COOKING_MANUAL_PROMPT),
        (
            "human",
            "Query dell'utente: \n\n {question}",
        ),
    ]
)
planet_distance_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", PLANET_DISTANCE_PROMPT),
        (
            "human",
            "Query dell'utente: \n\n {question}",
        ),
    ]
)

galactic_code_chain: RunnableSequence = galactic_code_prompt | structured_llm_generator  # type: ignore

cooking_manual_chain: RunnableSequence = (
    cooking_manual_prompt | structured_llm_generator
)  # type: ignore

llm = SessionManager().model_manager.model
planet_llm_generator = llm.with_structured_output(Planet)

planet_distance_chain: RunnableSequence = (
    planet_distance_prompt | structured_llm_generator
)  # type: ignore
