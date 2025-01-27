from langchain_core.tools import tool
from hackathon.models import Dish
from hackathon.managers.neo4j_store_manager import Neo4jStoreManager

neo4j_store_manager = Neo4jStoreManager()


@tool(name_or_callable="get_dishes_by_ingredient")
def get_dishes_by_ingredient(ingredient: str) -> dict[str, list[Dish]]:
    """Restituisce i piatti che contengono un ingrediente specifico"""
    query = """
    MATCH (d:Dish)
    WHERE $ingredient IN d.ingredients
    RETURN d
    """
    res = neo4j_store_manager.graph.query(
        query, params={"ingredient": ingredient.lower()}
    )
    return [Dish.from_neo4j(d) for d in res]


@tool(name_or_callable="get_dishes_by_ingredients")
def get_dishes_by_ingredients(ingredients: list[str]) -> list[Dish]:
    """Restituisce i piatti che contengono tutti gli ingredienti specificati"""
    query = """
    MATCH (d:Dish)
    WHERE ALL(ingredient IN $ingredients WHERE ingredient IN d.ingredients)
    RETURN d
    """
    res = neo4j_store_manager.graph.query(query, params={"ingredients": ingredients})
    return [Dish.from_neo4j(d) for d in res]


@tool(name_or_callable="get_dishes_by_planet")
def get_dishes_by_planet(planet_name: str) -> list[Dish]:
    """Restituisce i piatti preparati su un pianeta specifico"""
    query = """
    MATCH (d:Dish)
    WHERE d.planet_name = $planet_name
    RETURN d
    """
    res = neo4j_store_manager.graph.query(query, params={"planet_name": planet_name})
    return [Dish.from_neo4j(d) for d in res]


@tool(name_or_callable="get_dishes_by_custom_query")
def get_dishes_by_custom_query(query: str) -> list[Dish]:
    """Restituisce i piatti che soddisfano una query specifica"""
    res = neo4j_store_manager.graph.query(query)
    return [Dish.from_neo4j(d) for d in res]
