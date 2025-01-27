from typing import Any, Dict
import json
from hackathon.session import logger
from hackathon.graph.state import GraphState
from hackathon.utils.settings.settings_provider import SettingsProvider
from hackathon.session import SessionManager
from hackathon.graph.models import CSVEntry


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
        dish_id = dish_mapping.get(dish.dish_name, None)
        if dish_id is not None:
            dish_ids.append(str(dish_id))

    # Convert dish ids to strings
    print("Converting dish ids to strings")
    if len(dish_ids) == 0:
        result = "1"
    else:
        result = ",".join(dish_ids)

    # Add the entry to the dataset
    print("Adding entry to dataset")
    SessionManager().dataset_manager.add_entry(
        CSVEntry(question_id=state.question_id, result=result)
    )
    return {"question": state.question}
