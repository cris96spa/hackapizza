from langchain_core.tools import tool
from hackathon.models import Dish
from hackathon.session import SessionManager
from typing import Any

neo4j_store_manager = SessionManager().neo4j_manager


# @tool(name_or_callable="get_dishes_by_ingredients")
def get_dishes_by_ingredients(ingredients: list[str]) -> dict[str, list[Dish]]:
    """Restituisce i piatti che contengono tutti gli ingredienti specificati (case-insensitive).

    Esempi di utilizzo del tool:
    Input: Quali sono i piatti che includono le Chocobo Wings come ingrediente?
    Chain of Thoughts: La richiesta dell'utente richiede degli ingredienti specifici, posso utilizzare
    il tool `get_dishes_by_ingredients`con il seguente input: ['chocobo wings'].
    Chiamata al tool: get_dishes_by_ingredients(['chocobo wings']).
    """
    query = """
        MATCH (d:Dish)-[:CONTAINS]->(i:Ingredient)
        WHERE i.name IN $ingredients
        WITH d, COUNT(DISTINCT i) AS matched_ingredients
        WHERE matched_ingredients = SIZE($ingredients)
        RETURN d
        """
    res = neo4j_store_manager.graph.query(
        query, params={"ingredients": [i.lower() for i in ingredients]}
    )

    return {"dishes": _get_dishes(res)}


@tool(name_or_callable="get_dishes_by_planets")
def get_dishes_by_planets(planet_names: list[str]) -> dict[str, list[Dish]]:
    """Restituisce i piatti preparati sui pianeti specificati

    Esempi di utilizzo del tool:
    Input: "Quali piatti sono preparati su Cybertron e Krypton?"
    Chain of Thoughts: La richiesta dell'utente richiede i piatti preparati su due pianeti specifici, posso utilizzare
    il tool `get_dishes_by_planets` con il seguente input: ['cybertron', 'krypton'].
    Chiamata al tool: get_dishes_by_planets(['cybertron', 'krypton']).
    """

    query = """
    MATCH (d:Dish)
    WHERE d.planet_name IN $planet_names
    RETURN d
    """
    res = neo4j_store_manager.graph.query(
        query, params={"planet_names": [planet.lower() for planet in planet_names]}
    )

    return {"dishes": _get_dishes(res)}


@tool(name_or_callable="get_dishes_by_custom_query")
def get_dishes_by_custom_query(query: str, params: dict) -> dict[str, list[Dish]]:
    """Restituisce i piatti che soddisfano una query specifica.

    Esempi di utilizzo del tool:
    Input: "Quali piatti sono preparati utilizzando la tecnica della Sferificazione a Gravità Psionica Variabile?"
    Chain of Thoughts: La richiesta dell'utente richiede la presenza di una tecnica specifica, posso utilizzare il tool
    `get_dishes_by_custom_query` con la seguente query:
    ```
    query = MATCH (d:Dish)-[:REQUIRES_TECHNIQUE]->(t:Technique)
        WHERE t.name = $technique_name
        RETURN d
    ```
    e i seguenti parametri:
    ```
    params = {"technique_name": "sferificazione a gravità psionica variabile"}
    Chiamata al tool: get_dishes_by_custom_query(query)
    """

    # lower case all the parameters
    lower_params = {}
    for key, value in params.items():
        if isinstance(value, str):
            lower_params[key] = value.lower()
        else:
            lower_params[key] = value

    res = neo4j_store_manager.graph.query(query, lower_params)
    return {"dishes": _get_dishes(res)}


def _get_dishes(res: list[dict[str, Any]]) -> list[Dish]:
    dishes = []
    for d in res:
        dish_name = d[list(d.keys())[0]]["name"]
        ingredients = _get_ingredients_by_dish_name(dish_name)
        techniques = _get_techniques_by_dish_name(dish_name)
        dishes.append(Dish.from_neo4j(d, ingredients, techniques))
    return dishes


def _get_ingredients_by_dish_name(dish_name: str) -> list[str]:
    """Get the ingredients of a dish by its name.

    Args:
        - dish_name: Name of the dish.

    Returns:
        - List of ingredients.
    """
    query = """
        MATCH (d:Dish {name: $dish_name})-[:CONTAINS]->(i:Ingredient)
        RETURN i.name
        """
    res = neo4j_store_manager.graph.query(query, params={"dish_name": dish_name})
    return [r["i.name"] for r in res]


def _get_techniques_by_dish_name(dish_name: str) -> list[str]:
    """Get the techniques of a dish by its name.

    Args:
        - dish_name: Name of the dish.

    Returns:
        - List of techniques.
    """
    query = """
    MATCH (d:Dish {name: $dish_name}) -[:REQUIRES_TECHNIQUE] -> (t:Technique)
    RETURN t.name
    """
    res = neo4j_store_manager.graph.query(query, params={"dish_name": dish_name})
    return [r["t.name"] for r in res]


if __name__ == "__main__":
    ingredients = ["uova di fenice", "scaglie stellari"]
    dishes = get_dishes_by_ingredients(ingredients)
    print(dishes)
