from typing import Any, Dict
import json
from hackathon.session import logger
from hackathon.graph.state import GraphState
from hackathon.utils.settings.settings_provider import SettingsProvider
from hackathon.session import SessionManager
from hackathon.graph.models import CSVEntry
from langchain_core.documents import Document


def format_output(state: GraphState) -> Dict[str, Any]:
    print("---Format Output---")

    # Load the dish mapping
    print("Loading dish mapping")
    mapping_path = SettingsProvider().get_dish_mapping_path()
    with open(mapping_path) as file:
        dish_mapping = json.load(file)

    # Get the dishes from the state
    dishes = state.dishes
    dish_ids = []

    # Map the dishes to ids
    print("Mapping dishes to ids")
    for dish in dishes:
        dish_id = dish_mapping.get(dish, None)
        if dish_id is not None:
            dish_ids.append(str(dish_id))

    # Convert dish ids to strings
    print("Converting dish ids to strings")
    result = ",".join(dish_ids)

    # Add the entry to the dataset
    print("Adding entry to dataset")
    SessionManager().dataset_manager.add_entry(
        CSVEntry(question_id=state.question_id, result=result)
    )
    return {"question": state.question}


if __name__ == "__main__":
    from langchain.schema import Document

    for i in range(10):
        state = GraphState(
            question="The question asked by the user",
            question_id=i + 1,
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
        format_output(state)

    SessionManager().dataset_manager.dataset
