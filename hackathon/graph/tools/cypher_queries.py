from langchain_core.tools import tool
from hackathon.models import Dish
from hackathon.managers.neo4j_store_manager import Neo4jStoreManager

neo4j_store_manager = Neo4jStoreManager()


@tool(name_or_callable="get_dishes_by_ingredients")
def get_dishes_by_ingredients(ingredients: list[str]) -> dict[str, list[Dish]]:
    """Restituisce i piatti che contengono tutti gli ingredienti specificati (case-insensitive).

    Esempi di utilizzo del tool:
    Input: Quali sono i piatti che includono le Chocobo Wings come ingrediente?
    Chain of Thoughts: La richiesta dell'utente richiede degli ingredienti specifici, posso utilizzare
    il tool `get_dishes_by_ingredients`con il seguente input: ['Chocobo Wings'].
    Chiamata al tool: get_dishes_by_ingredients(['Chocobo Wings']).
    """
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


@tool(name_or_callable="get_dishes_by_planets")
def get_dishes_by_planets(planet_names: list[str]) -> dict[str, list[Dish]]:
    """Restituisce i piatti preparati sui pianeti specificati (case-insensitive)

    Esempi di utilizzo del tool:
    Input: "Quali piatti sono preparati su Cybertron e Krypton?"
    Chain of Thoughts: La richiesta dell'utente richiede i piatti preparati su due pianeti specifici, posso utilizzare
    il tool `get_dishes_by_planets` con il seguente input: ['Cybertron', 'Krypton'].
    Chiamata al tool: get_dishes_by_planets(['Cybertron', 'Krypton']).
    """

    query = """
    MATCH (d:Dish)
    WHERE toLower(d.planet_name) IN [name IN $planet_names | toLower(name)]
    RETURN d
    """
    res = neo4j_store_manager.graph.query(query, params={"planet_names": planet_names})
    if not len(res):
        return {"dishes": []}
    return {"dishes": [Dish.from_neo4j(d) for d in res]}


@tool(name_or_callable="get_dishes_by_custom_query")
def get_dishes_by_custom_query(query: str) -> dict[str, list[Dish]]:
    """Restituisce i piatti che soddisfano una query specifica.

    Esempi di utilizzo del tool:
    Input: "Quali piatti sono preparati utilizzando la tecnica della Sferificazione a Gravità Psionica Variabile?"
    Chain of Thoughts: La richiesta dell'utente richiede la presenza di una tecnica specifica, posso utilizzare il tool
    `get_dishes_by_custom_query` con la seguente query:
    "
        MATCH (d:Dish)
        WHERE toLower("Sferificazione a Gravità Psionica Variabile") IN [x IN d.techniques | toLower(x)]
        RETURN
        d
    "
    Chiamata al tool: get_dishes_by_custom_query(query)
    """
    res = neo4j_store_manager.graph.query(query)
    if not len(res):
        return {"dishes": []}
    return {"dishes": [Dish.from_neo4j(d) for d in res]}
