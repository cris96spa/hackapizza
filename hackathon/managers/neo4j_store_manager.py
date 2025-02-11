from langchain_neo4j import Neo4jGraph
from tqdm import tqdm
from hackathon.utils.file_utils import load_json
from hackathon.models import Dish, Chef, Technique
import json
from hackathon.utils.settings.settings_provider import SettingsProvider
import logging

logger = logging.getLogger(__name__)


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
        """Add a dish to the graph.

        Args:
            - dish: Dish object.
        """

        query = """
        MERGE (d:Dish {name: $name})
        SET d.restaurant = $restaurant, 
            d.chef_name = $chef_name, 
            d.planet_name = $planet_name,
            d.dish_id = $dish_id,
            d.culinary_order = $culinary_order

        MERGE (c:Chef {name: $chef_name, restaurant: $restaurant, planet_name: $planet_name})
        MERGE (d)-[:CREATED_BY]->(c)
        """

        params = {
            "name": dish.name.lower(),
            "restaurant": dish.restaurant.lower(),
            "chef_name": dish.chef_name.lower(),
            "planet_name": dish.planet_name.lower(),
            "dish_id": str(self.dish_mapping.get(dish.name.lower(), "-1")),
            "culinary_order": dish.culinary_order,
        }

        self.graph.query(query, params)

        # Add Ingredient Relationships
        for ingredient in dish.ingredients:
            ing_query = """
            MERGE (i:Ingredient {name: $ingredient_name})
            MERGE (d:Dish {name: $name})
            MERGE (d)-[:CONTAINS]->(i)
            """
            ing_params = {
                "name": dish.name.lower(),
                "ingredient_name": ingredient.lower(),
            }
            self.graph.query(ing_query, ing_params)

        # Add Technique Relationships
        for technique in dish.techniques:
            tech_query = """
            MERGE (t:Technique {name: $technique_name})
            MERGE (d:Dish {name: $name})
            MERGE (d)-[:REQUIRES_TECHNIQUE]->(t)
            """
            tech_params = {
                "name": dish.name.lower(),
                "technique_name": technique.lower(),
            }
            self.graph.query(tech_query, tech_params)

    def add_dishes(self, dishes: list[Dish]) -> None:
        """Add a list of dishes to the graph.

        Args:
            - dishes: list of Dish objects.
        """
        for dish in tqdm(dishes, desc="Adding dishes"):
            self._add_dish(dish)
        logger.info(f"Added {len(dishes)} dishes to the graph.")

    def add_techniques(self, techniques: list[Technique]) -> None:
        """Add a list of techniques to the graph.

        Args:
            - techniques: list of Technique objects.
        """
        for technique in tqdm(techniques, desc="Adding techniques"):
            self._add_technique(technique)

        logger.info(f"Added {len(techniques)} techniques to the graph.")

    def _add_technique(self, technique: Technique) -> None:
        """Add a technique to the graph.

        Args:
            - technique: Technique object.
        """
        query = """
        MERGE (t:Technique {name: $name, category: $category})
        SET t.category = $category

        FOREACH (license IN $licenses |
            MERGE (l:License {name: license.name, level: license.level})
            SET l.level = license.level
            MERGE (t)-[:NEEDS_LICENSE]->(l)
        )
        """

        params = {
            "name": technique.name.lower(),
            "category": technique.category.lower(),
            "licenses": [
                {"name": lic.name.lower(), "level": lic.level}
                for lic in technique.licenses
            ],
        }

        self.graph.query(query, params)

    def _add_chef(self, chef: Chef) -> None:
        """Add a chef to the graph.

        Args:
            - chef: Chef object.
        """
        query = """
        MERGE (c:Chef {name: $name, restaurant: $restaurant})
        SET c.restaurant = $restaurant, 
            c.name = $name,
            c.planet_name = $planet_name
        
        FOREACH (license IN $licenses |
            MERGE (l:License {name: license.name, level: license.level})
            SET l.level = license.level,
                l.name = license.name
            MERGE (c)-[:HOLDS_LICENSE]->(l)
        )
        """

        params = {
            "name": chef.name.lower(),
            "restaurant": chef.restaurant.lower(),
            "planet_name": chef.planet_name.lower(),
            # "document": chef.document,
            "licenses": [
                {"name": lic.name.lower(), "level": lic.level} for lic in chef.licenses
            ],
        }

        self.graph.query(query, params)

    def add_chefs(self, chefs: list[Chef]) -> None:
        """Add a list of chefs to the graph.

        Args:
            - chefs: list of Chef objects.
        """
        for chef in tqdm(chefs, desc="Adding chefs"):
            self._add_chef(chef)

        logger.info(f"Added {len(chefs)} chefs to the graph.")

    def reset_graph(self) -> None:
        self.graph.query("MATCH (n) DETACH DELETE n")

    def setup(self) -> None:
        """Setup the graph by loading the data from the JSON files."""

        # Check for consistency
        check_consistency()

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
    """
    Check if all the dishes and techniques are mapped. This is useful to check
    if all the data is consistent and can be loaded into the graph.
    """
    # Load the dish mapping
    mapping_path = SettingsProvider().get_dish_mapping_path()
    with open(mapping_path) as file:
        dish_mapping = json.load(file)

    # Load the dishes
    dishes = [
        Dish.model_validate(dish)
        for dish in load_json(SettingsProvider().get_dishes_json_path())
    ]

    # Load the chefs
    chefs = [
        Chef.model_validate(chef)
        for chef in load_json(SettingsProvider().get_chefs_json_path())
    ]

    # Load the techniques
    techniques = [
        Technique.model_validate(technique)
        for technique in load_json(SettingsProvider().get_techniques_json_path())
    ]
    technique_names = set(technique.name.lower() for technique in techniques)

    # Assert that techniques are consistent
    dish_techniques = set()
    for dish in dishes:
        for technique in dish.techniques:
            dish_techniques.add(technique.lower())

    assert dish_techniques - technique_names == set()
    logger.info(
        f"{len(dish_techniques - technique_names)} techniques not mapped. {dish_techniques - technique_names}"
    )

    # Assert that all the dishes are mapped
    dish_names = set(dish.name.lower() for dish in dishes)
    true_dish_names = set(dish_mapping.keys())
    assert dish_names - true_dish_names == set()

    logger.info(
        f"{len(dish_names - true_dish_names)} dishes not mapped: {dish_names - true_dish_names}"
    )

    # Assert that all the chefs are consistent
    chef_names = set(chef.name.lower() for chef in chefs)
    chef_names_dishes = set(dish.chef_name.lower() for dish in dishes)

    assert chef_names_dishes - chef_names == chef_names_dishes - chef_names == set()
    logger.info(
        f"{len(chef_names_dishes - chef_names)} chefs not found: {chef_names_dishes - chef_names}"
    )


if __name__ == "__main__":
    neo4j_store_manager = Neo4jStoreManager(reset_graph=True)

    # Dish.from_neo4j(retrieved_dishes[0])

    # model = ModelManager().model

    # techniques = load_json(SettingsProvider().get_techniques_json_path())
    # tech = []

    # for key in techniques.keys():
    #     tech.append(Technique(name=key, category=techniques[key]))
    # save_json(tech, SettingsProvider().get_techniques_json_path())
