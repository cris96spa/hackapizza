from typing import Any, Dict
from hackathon.graph.state import GraphState
from hackathon.session import SessionManager
from hackathon.graph.chains.query_metadata_extractor import menu_metadata_extractor
from hackathon.models import MenuMetadata, menu_metadata_keys


def extract_metadata(state: GraphState) -> Dict[str, Any]:
    """
    Retrieve documents from the vector store.

    Args:
        state: The current state of the graph.

    Returns:
        A dictionary containing the retrieved documents.
    """

    menu_metadata = menu_metadata_extractor.invoke(
        {
            "document": state.question,
            "metadata_possible_values": state.vector_db_key_values,
        }
    )
    return {"menu_metadata": menu_metadata}


if __name__ == "__main__":
    from langchain.schema import Document

    state = GraphState(
        question="Quali piatti possono essere trovati, preparati da uno chef con almeno la licenza P di grado 5, che includono Teste di Idra o che sono realizzati utilizzando la tecnica della Bollitura Entropica Sincronizzata?",
        question_id=1,
        generation="The LLM generation.",
        documents=[Document(page_content="The content of the page")],
        dishes=[
            "Il Viaggio Celeste",
            "Il Viaggio Cosmico di Marinetti",
            "Il Viaggio dell'Etereo Risveglio",
            "Il Viaggio delle Dimensioni Confluenti",
            "Interstellar Requiem",
            "Interstellare Risveglio di Kraken",
            "L'Abbraccio del Cosmo",
            "L'Ascensione Siderale",
            "L'Estasi Cosmica di Nova",
            "L'Eternit\u00e0 al Crepuscolo",
        ],
    )
    extract_metadata(state)
