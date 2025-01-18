from typing import Any, Dict

from hackathon.graph.chains.generation import generator
from hackathon.graph.models import GenerationResponse
from hackathon.graph.state import GraphState
from hackathon.utils.formatter import Formatter


def generate(state: GraphState) -> Dict[str, Any]:
    print("---GENERATE---")
    question = state.question
    documents = state.documents

    generation: GenerationResponse = generator.invoke(
        {"question": question, "documents": documents}
    )

    return {
        "dishes": generation.dishes,
    }
