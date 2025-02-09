from langchain_neo4j import Neo4jGraph
from langchain_core.tools import tool
from tqdm import tqdm
from hackathon.utils.file_utils import load_json, save_json
from hackathon.models import Dish, Chef, Technique, License
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
        MERGE (d:Dish {name: $dish_name})
        SET d.restaurant = $restaurant, 
            d.chef_name = $chef_name, 
            d.planet_name = $planet_name,
            d.dish_id = $dish_id

        MERGE (c:Chef {name: $chef_name, restaurant: $restaurant})
        MERGE (d)-[:PREPARED_BY]->(c)
        """

        params = {
            "dish_name": dish.dish_name.lower(),
            "restaurant": dish.restaurant.lower(),
            "chef_name": dish.chef_name.lower(),
            "planet_name": dish.planet_name.lower(),
            "dish_id": str(self.dish_mapping.get(dish.dish_name.lower(), "-1")),
        }

        self.graph.query(query, params)
        print(f"Added dish {dish.dish_name}")

        # Add Ingredient Relationships
        for ingredient in dish.ingredients:
            ing_query = """
            MERGE (i:Ingredient {name: $ingredient_name})
            MERGE (d:Dish {name: $dish_name})
            MERGE (d)-[:USES]->(i)
            """
            ing_params = {
                "dish_name": dish.dish_name.lower(),
                "ingredient_name": ingredient.lower(),
            }
            self.graph.query(ing_query, ing_params)

        # Add Technique Relationships
        for technique in dish.techniques:
            tech_query = """
            MERGE (t:Technique {name: $technique_name})
            MERGE (d:Dish {name: $dish_name})
            MERGE (d)-[:REQUIRES]->(t)
            """
            tech_params = {
                "dish_name": dish.dish_name.lower(),
                "technique_name": technique.lower(),
            }
            self.graph.query(tech_query, tech_params)

        print(f"Linked dish {dish.dish_name} to ingredients and techniques.")

    def add_dishes(self, dishes: list[Dish]) -> None:
        for dish in tqdm(dishes):
            self._add_dish(dish)

    def add_techniques(self, techniques: list[Technique]) -> None:
        for technique in tqdm(techniques):
            self._add_technique(technique)

    def _add_technique(self, technique: Technique) -> None:
        query = """
        MERGE (t:Technique {name: $name})
        SET t.category = $category

        MERGE (c:Category {name: $category})
        MERGE (t)-[:BELONGS_TO]->(c)
        """

        params = {
            "name": technique.name.lower(),
            "category": technique.category.lower(),
        }

        self.graph.query(query, params)
        print(f"Added technique {technique.name} in category {technique.category}")

    def _add_chef(self, chef: Chef) -> None:
        query = """
        MERGE (c:Chef {name: $name})
        SET c.restaurant = $restaurant, 
            c.document = $document,
            c.name = $name,
            c.planet_name = $planet_name,
            c.licenses = $licenses
        
        FOREACH (license IN $licenses_dict |
            MERGE (l:License {name: license.name, level: license.level})
            SET l.name = license.name, 
                l.level = license.level
            MERGE (c)-[:HAS_LICENSE]->(l)
        )
        """

        params = {
            "name": chef.name.lower(),
            "restaurant": chef.restaurant.lower(),
            "planet_name": chef.planet_name.lower(),
            "document": chef.document,
            "licenses": json.dumps([license.model_dump() for license in chef.licenses]),
            "licenses_dict": [license.model_dump() for license in chef.licenses],
        }

        self.graph.query(query, params)
        print(f"Added chef {chef.name} with licenses directly stored.")

    def add_chefs(self, chef: list[Chef]) -> None:
        for chef in tqdm(chef):
            self._add_chef(chef)

    def reset_graph(self) -> None:
        self.graph.query("MATCH (n) DETACH DELETE n")

    def setup(self) -> None:
        techniques = [
            Technique.model_validate(technique)
            for technique in load_json(SettingsProvider().get_techniques_json_path())
        ]
        self.add_techniques(techniques)

        # Load chefs
        chefs = [
            Chef.model_validate(chef)
            for chef in load_json(SettingsProvider().get_chefs_json_path())
        ]
        self.add_chefs(chefs)

        # Load dishes
        dishes = [
            Dish.model_validate(dish)
            for dish in load_json(SettingsProvider().get_dishes_json_path())
        ]
        self.add_dishes(dishes)


def check_consistency():
    # Load the dish mapping
    mapping_path = SettingsProvider().get_dish_mapping_path()
    with open(mapping_path) as file:
        dish_mapping = json.load(file)

    # Load the dishes
    dishes = [
        Dish.model_validate(dish)
        for dish in load_json(SettingsProvider().get_dishes_json_path())
    ]

    # Load the techniques
    techniques = set()
    for dish in dishes:
        for technique in dish.techniques:
            techniques.add(technique.lower())

    # Load the mapping
    mapping = load_json(SettingsProvider().get_techniques_json_path())

    # Check if all techniques are mapped
    not_mapped = []
    for technique in techniques:
        if technique not in mapping:
            not_mapped.append(technique)

    print(f"{len(not_mapped)} techniques not mapped.")

    # Check if all dishes have a mapping
    not_mapped = []
    for dish in dishes:
        if dish.dish_name.lower() not in dish_mapping:
            not_mapped.append(dish.dish_name)

    print(f"{len(not_mapped)} dishes not mapped: {not_mapped}")


if __name__ == "__main__":
    # neo4j_store_manager = Neo4jStoreManager(reset_graph=True)
    # retrieved_dishes = neo4j_store_manager.graph.query("MATCH (d:Dish) RETURN d")
    # Dish.from_neo4j(retrieved_dishes[0])

    # model = ModelManager().model
    # check_consistency()
    # techniques = load_json(SettingsProvider().get_techniques_json_path())
    # tech = []

    # for key in techniques.keys():
    #     tech.append(Technique(name=key, category=techniques[key]))
    # save_json(tech, SettingsProvider().get_techniques_json_path())

    techniques = load_json(SettingsProvider().get_techniques_json_path())
    print(len(techniques))
    path = "competition_data/entities/licenses_techniques.json"
    tech_licenses = load_json(path)
    for technique in techniques:
        licenses = list(
            filter(
                lambda x: x["technique"].lower() == technique["name"].lower(),
                tech_licenses,
            )
        )[0]
        technique["licenses"] = licenses["licenses"]
    save_json(techniques, SettingsProvider().get_techniques_json_path())
