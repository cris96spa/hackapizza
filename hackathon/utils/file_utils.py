from pydantic import BaseModel
import json
import os


def save_json(entities: list[BaseModel], path: str) -> None:
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    if isinstance(entities, list):
        if len(entities) and isinstance(entities[0], BaseModel):
            entities_dict = [entity.model_dump() for entity in entities]
        else:
            raise ValueError(
                "Invalid entities type. Expected a non empty list of BaseModel"
            )
    elif isinstance(entities, dict):
        entities_dict = entities
    else:
        raise ValueError("Invalid entities type")
    with open(path, "w") as f:
        json.dump(entities_dict, f, indent=4)


def load_json(file_path: str) -> list:
    with open(file_path, "r") as file:
        return json.load(file)
