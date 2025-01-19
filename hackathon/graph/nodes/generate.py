from typing import Any, Dict

from hackathon.graph.chains.generation import generator
from hackathon.graph.models import GenerationResponse
from hackathon.graph.state import GraphState
from hackathon.utils.formatter import Formatter
from langchain.prompts import ChatPromptTemplate
from hackathon.graph.prompts import GENERATION_PROMPT
from langchain_core.runnables import RunnableSequence
from hackathon.session import SessionManager


def generate(state: GraphState) -> Dict[str, Any]:
    print("---GENERATE---")
    question = state.question
    documents = state.documents

    llm = SessionManager().model_manager.model
    structured_llm_generator = llm.with_structured_output(GenerationResponse)
    messages = [
        ("system", GENERATION_PROMPT),
        (
            "human",
            "User query: \n\n {question} \n\n Context: {documents}",
        ),
    ]

    if len(state.code_documents) > 0:
        messages.append(
            (
                "system",
                "Considera anche il seguente contesto inerente il Codice Galattico. Utilizza i metadati per filtrare i risultati.",
            )
        )
        for doc in state.code_documents:
            messages.append(("system", Formatter.format_document(doc)))

    if len(state.manual_documents) > 0:
        messages.append(
            (
                "system",
                "Considera anche il seguente contesto inerente il Manuale di Cucina. Utilizza i metadati per filtrare i risultati.",
            )
        )
        for doc in state.manual_documents:
            messages.append(("system", Formatter.format_document(doc)))

    if len(state.near_planets) > 0:
        messages.append(
            (
                "system",
                "I piatti in considerazione devono provenire esclusivamente dai seguenti pianeti, utilizza i metadati per filtrare i risultati:",
            )
        )
        for doc in state.near_planets:
            messages.append(("system", Formatter.format_document(doc)))

    generation_prompt = ChatPromptTemplate.from_messages(messages)

    generator: RunnableSequence = generation_prompt | structured_llm_generator  # type: ignore

    generation: GenerationResponse = generator.invoke(
        {"question": question, "documents": documents}
    )

    return {
        "dishes": generation.dishes,
    }
