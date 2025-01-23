from langchain.schema import Document
from hackathon.ingestion.menu import MenuIngestor
from hackathon.ingestion.galactic_code import GalacticCodeIngestor
from hackathon.ingestion.cooking_manual import CookingManualIngestor
from hackathon.utils.settings.settings_provider import SettingsProvider
from tqdm import tqdm
import os
from pydantic import BaseModel
import json

from hackathon.graph.chains.extract_entities import (
    chef_extraction_chain,
    dish_extraction_chain,
)

from hackathon.models import Chef, Dish


class Parser:
    def __init__(self):
        self.settings_provider = SettingsProvider()

    def _parse_menu(self) -> None:
        menu_path = self.settings_provider.get_menu_path()

        if not os.path.exists(menu_path):
            raise FileNotFoundError(f"Menu file not found at path: {menu_path}")

        # Load the menu documents
        menu_file_names = [
            file
            for file in os.listdir(menu_path)
            if os.path.isfile(os.path.join(menu_path, file))
        ]

        # Define the menu ingestor
        menu_ingestor = MenuIngestor()

        chefs = []
        dishes = []

        # Scan the menu files
        for menu in tqdm(menu_file_names, desc="Parsing menu document to markdown"):
            # Load all chunks of the given menu
            menu_splits = menu_ingestor.ingest(os.path.join(menu_path, menu))

            # Take the first chunk as the header
            header = menu_splits[0]

            # call llm to extract chef information

            chef: Chef = chef_extraction_chain.invoke(
                {
                    "document": header,
                }
            )

            chef.restaurant = menu.split(".")[0].lower()
            chef.document = header
            chefs.append(chef)

            # parse each dish in the menu
            for chunk in menu_splits[1:]:
                dish: Dish = dish_extraction_chain.invoke(
                    {
                        "document": chunk,
                    }
                )
                dish.restaurant = chef.restaurant
                dish.chef_name = chef.name
                dish.planet_name = chef.planet_name
                dish.document = chunk.page_content
                dishes.append(dish)

        self._save_json(chefs, self.settings_provider.get_chefs_json_path())
        self._save_json(dishes, self.settings_provider.get_dishes_json_path())

    def _save_json(self, entities: list[BaseModel], path: str) -> None:
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        entities_dict = [entity.model_dump() for entity in entities]
        with open(path, "w") as f:
            json.dump(entities_dict, f, indent=4)


# def _load_source_of_truth(self) -> list[Document]:
#     recursive_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
#         chunk_size=256, chunk_overlap=0
#     )
#     galactic_code_documents = GalacticCodeIngestor().ingest(
#         self.settings_provider.get_galactic_code_path()
#     )

#     galactic_code_splits = []
#     for doc in tqdm(
#         galactic_code_documents,
#         desc="Adding galactic code documents to vectorstore",
#     ):
#         galactic_code_splits = recursive_splitter.split_documents([doc])
#         for split in galactic_code_splits:
#             split.metadata.update({"is_code": True})
#             split.page_content = Formatter.format_document(split)

#     cooking_manual_documents = CookingManualIngestor().ingest(
#         self.settings_provider.get_cooking_manual_path()
#     )

#     cooking_manual_splits = []
#     for doc in tqdm(
#         cooking_manual_documents,
#         desc="Adding cooking manual documents to vectorstore",
#     ):
#         cooking_manual_splits = recursive_splitter.split_documents([doc])
#         for split in cooking_manual_splits:
#             split.page_content = Formatter.format_document(split)
#             split.metadata.update({"is_manual": True})

#     documents = galactic_code_splits + cooking_manual_splits

#     return documents


def main():
    parser = Parser()
    parser._parse_menu()


if __name__ == "__main__":
    main()
