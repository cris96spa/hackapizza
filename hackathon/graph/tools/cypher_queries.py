from langchain_core.tools import tool
from hackathon.models import Dish
from hackathon.managers.neo4j_store_manager import Neo4jStoreManager

neo4j_store_manager = Neo4jStoreManager()


@tool(name_or_callable="get_dishes_by_ingredients")
def get_dishes_by_ingredients(ingredients: list[str]) -> dict[str, list[Dish]]:
    """Restituisce i piatti che contengono tutti gli ingredienti specificati (case-insensitive)"""
    query = """
    MATCH (d:Dish)
    WHERE ALL(ingredient IN $ingredients WHERE toLower(ingredient) IN [x IN d.ingredients | toLower(x)])
    RETURN d
    """
    res = neo4j_store_manager.graph.query(
        query, params={"ingredients": [i for i in ingredients]}
    )
    if not len(res):
        return {"dishes": []}
    return {"dishes": [Dish.from_neo4j(d) for d in res]}


@tool(name_or_callable="get_dishes_by_planet")
def get_dishes_by_planet(planet_name: str) -> dict[str, list[Dish]]:
    """Restituisce i piatti preparati su un pianeta specifico (case-insensitive)"""
    query = """
    MATCH (d:Dish)
    WHERE toLower(d.planet_name) = toLower($planet_name)
    RETURN d
    """
    res = neo4j_store_manager.graph.query(query, params={"planet_name": planet_name})
    if not len(res):
        return {"dishes": []}
    return {"dishes": [Dish.from_neo4j(d) for d in res]}


@tool(name_or_callable="get_dishes_by_custom_query")
def get_dishes_by_custom_query(query: str) -> dict[str, list[Dish]]:
    """Restituisce i piatti che soddisfano una query specifica"""
    res = neo4j_store_manager.graph.query(query)
    if not len(res):
        return {"dishes": []}
    return {"dishes": [Dish.from_neo4j(d) for d in res]}
