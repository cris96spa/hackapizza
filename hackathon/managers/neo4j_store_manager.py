from langchain_neo4j import Neo4jGraph
from langchain_core.tools import tool
from tqdm import tqdm
from hackathon.utils.file_utils import load_json
from hackathon.models import Dish, Chef
import json
from hackathon.utils.settings.settings_provider import SettingsProvider
from hackathon.managers.model_manager import ModelManager
from langchain_core.prompts import ChatPromptTemplate


class Neo4jStoreManager:
    def __init__(self, reset_graph: bool = False):
        self.settings_provider = SettingsProvider()
        self.graph = Neo4jGraph(
            url=self.settings_provider.get_neo4j_url(),
            username=self.settings_provider.get_neo4j_username(),
            password=self.settings_provider.get_neo4j_password(),
        )
        if reset_graph:
            # Load the dish mapping
            mapping_path = SettingsProvider().get_dish_mapping_path()
            with open(mapping_path) as file:
                dish_mapping = json.load(file)
            self.dish_mapping = dish_mapping

            self.reset_graph()
            self.setup()

    def _add_dish(self, dish: Dish) -> None:
        query = """
        MERGE (d:Dish {dish_name: $dish_name})
        SET d.restaurant = $restaurant, 
            d.chef_name = $chef_name, 
            d.planet_name = $planet_name,
            d.dish_id = $dish_id, 
            d.ingredients = $ingredients, 
            d.techniques = $techniques

        MERGE (c:Chef {name: $chef_name, restaurant: $restaurant})
        MERGE (d)-[:PREPARED_BY]->(c)
        """
        params = {
            "dish_name": dish.dish_name,
            "restaurant": dish.restaurant,
            "chef_name": dish.chef_name,
            "planet_name": dish.planet_name,
            "dish_id": str(self.dish_mapping.get(dish.dish_name.lower(), "-1")),
            "ingredients": [ingredient for ingredient in dish.ingredients],
            "techniques": [technique for technique in dish.techniques],
        }
        self.graph.query(query, params=params)
        print(f"Added dish {dish.dish_name}")

    def add_dishes(self, dishes: list[Dish]) -> None:
        for dish in tqdm(dishes):
            self._add_dish(dish)

    def _add_chef(self, chef: Chef) -> None:
        query = """
            MERGE (c:Chef {name: $name})
            SET c.restaurant = $restaurant, 
                c.document = $document,
                c.name = $name,
                c.planet_name = $planet_name,
                c.licenses = $licenses
            
            FOREACH (license in $licenses_dict |
                MERGE (l:License {name: license.name, level: license.level})
                SET l.name = license.name, 
                    l.level = license.level
                MERGE (c)-[:HAS_LICENSE]->(l)
            )
        """

        # Prepare parameters
        params = {
            "name": chef.name,
            "restaurant": chef.restaurant,
            "planet_name": chef.planet_name,
            "document": chef.document,
            "licenses": json.dumps([license.model_dump() for license in chef.licenses]),
            "licenses_dict": [license.model_dump() for license in chef.licenses],
        }

        self.graph.query(query, params=params)
        print(f"Added chef {chef.name} with licenses directly stored.")

    def add_chefs(self, chef: list[Chef]) -> None:
        for chef in tqdm(chef):
            self._add_chef(chef)

    def reset_graph(self) -> None:
        self.graph.query("MATCH (n) DETACH DELETE n")

    def setup(self) -> None:
        # Load dishes
        dishes = [
            Dish.model_validate(dish)
            for dish in load_json(SettingsProvider().get_dishes_json_path())
        ]
        self.add_dishes(dishes)

        # Load chefs
        chefs = [
            Chef.model_validate(chef)
            for chef in load_json(SettingsProvider().get_chefs_json_path())
        ]
        self.add_chefs(chefs)


if __name__ == "__main__":
    neo4j_store_manager = Neo4jStoreManager(reset_graph=True)
    retrieved_dishes = neo4j_store_manager.graph.query("MATCH (d:Dish) RETURN d")
    Dish.from_neo4j(retrieved_dishes[0])

    model = ModelManager().model
