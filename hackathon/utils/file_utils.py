from pydantic import BaseModel
import json
import os


def save_json(entities: list[BaseModel], path: str) -> None:
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    entities_dict = [entity.model_dump() for entity in entities]
    with open(path, "w") as f:
        json.dump(entities_dict, f, indent=4)


def load_json(file_path: str) -> list:
    with open(file_path, "r") as file:
        return json.load(file)
