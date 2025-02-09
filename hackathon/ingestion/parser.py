from langchain.schema import Document
from hackathon.ingestion.menu import MenuIngestor
from hackathon.ingestion.galactic_code import GalacticCodeIngestor
from hackathon.ingestion.cooking_manual import CookingManualIngestor
from hackathon.utils.settings.settings_provider import SettingsProvider
from tqdm import tqdm
import time
import os
from pydantic import BaseModel
from hackathon.utils.file_utils import load_json

from hackathon.graph.chains.extract_entities import (
    chef_extraction_chain,
    dish_extraction_chain,
)

from hackathon.models import Chef, Dish
from hackathon.utils.file_utils import save_json


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

        techniques_mapping = load_json(
            self.settings_provider.get_techniques_json_path()
        )
        techniques = list(techniques_mapping.keys())
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
            chef.document = header.page_content
            chefs.append(chef)

            # parse each dish in the menu
            for chunk in menu_splits[1:]:
                dish: Dish = dish_extraction_chain.invoke(
                    {
                        "document": chunk,
                        "techniques": techniques,
                    }
                )
                dish.restaurant = chef.restaurant
                dish.chef_name = chef.name
                dish.planet_name = chef.planet_name
                dish.document = chunk.page_content
                dishes.append(dish)
                time.sleep(3)

        save_json(chefs, self.settings_provider.get_chefs_json_path())
        save_json(dishes, self.settings_provider.get_dishes_json_path())


def main():
    parser = Parser()
    parser._parse_menu()


if __name__ == "__main__":
    # main()
    pass
