from pydantic import BaseModel, Field
from typing import Literal, Any
import json


# region Entities
class Dish(BaseModel):
    """Definisce un piatto"""

    dish_id: str | None = Field(
        description="L'identificativo del piatto.", default=None
    )
    name: str | None = Field(description="Il nome del piatto.", default=None)
    restaurant: str | None = Field(description="Il nome del ristorante.", default=None)
    chef_name: str | None = Field(description="Il nome del chef.", default=None)
    planet_name: str | None = Field(description="Il nome del pianeta.", default=None)
    ingredients: list[str] = Field(
        description="Gli ingredienti del piatto.", default_factory=[]
    )
    techniques: list[str] = Field(
        description="Le tecniche di preparazione del piatto.", default_factory=[]
    )
    document: str | None = Field(
        description="Questo campo deve rimanere vuoto. E' utilizzato per contenere il contesto. Non riempirlo.",
        default=None,
    )
    culinary_order: Literal[
        "ordine della galassia di andromeda",
        "ordine dei naturalisti",
        "ordine degli armonisti",
        "nessun ordine",
    ] = Field(description="L'ordine culinario del piatto.", default="nessun ordine")

    @classmethod
    def from_neo4j(
        cls,
        dish_data: dict[str, Any],
        ingredients_data: list[str],
        techniques_data: list[str],
    ) -> "Dish":
        """Converte un dizionario ottenuto da Neo4j in un oggetto Dish"""
        dish_data = dish_data[list(dish_data.keys())[0]]

        return cls(
            name=dish_data.get("name", ""),
            restaurant=dish_data.get("restaurant", ""),
            chef_name=dish_data.get("chef_name", ""),
            planet_name=dish_data.get("planet_name", ""),
            ingredients=ingredients_data,
            techniques=techniques_data,
            dish_id=dish_data.get("dish_id", ""),
            culinary_order=dish_data.get("culinary_order", "nessun ordine"),
            document=dish_data.get("document", ""),
        )


class License(BaseModel):
    """Definisce una licenza"""

    name: Literal[
        "psionica",
        "temporale",
        "gravitazionale",
        "antimateria",
        "magnetica",
        "quantistica",
        "luce",
        "sviluppo tecnologico",
    ] = Field(description="Il nome della licenza.")
    level: int = Field(description="Il livello della licenza.", default=0, ge=0)


class Technique(BaseModel):
    name: str = Field(description="Il nome della tecnica di preparazione.")
    category: Literal[
        "grigliatura",
        "cottura a vapore",
        "affumicatura",
        "tecniche di taglio",
        "forno",
        "saltare in padella",
        "surgelamento",
        "tecniche di impasto",
        "marinatura",
        "fermentazione",
        "sferificazione",
        "bollitura",
        "decostruzione",
        "sottovuoto",
    ] = Field(description="La categoria della tecnica di preparazione.")
    licenses: list[License] = Field(
        description="Le licenze necessarie per utilizzare la tecnica."
    )


class Chef(BaseModel):
    """Definisce un chef"""

    name: str = Field(description="Il nome del chef.")
    restaurant: str = Field(description="Il nome del ristorante.")
    licenses: list[License] = Field(description="Le licenze del chef.")
    planet_name: str = Field(description="Il nome del pianeta.")
    document: str | None = Field(
        description="Questo campo deve rimanere vuoto. E' utilizzato per contenere il contesto. Non riempirlo.",
        default=None,
    )

    @classmethod
    def from_neo4j(cls, data: dict[str, Any]) -> "Chef":
        """Converte un dizionario ottenuto da Neo4j in un oggetto Chef.
        La complessità risiende nella definizione delle licenze. In Neo4j le licenze sono
        salvate come stringa Json corrispondente alla serializzazione di una lista di dizionari.
        """
        chef_data = data[list(data.keys())[0]]
        licenses = json.loads(chef_data.get("licenses", "[]"))
        parsed_licenses = [License.model_validate(license) for license in licenses]
        return cls(
            name=chef_data.get("name", ""),
            restaurant=chef_data.get("restaurant", ""),
            planet_name=chef_data.get("planet_name", ""),
            document=chef_data.get("document", ""),
            licenses=parsed_licenses,
        )


# endregion

# region Planet


class Planet(BaseModel):
    name: str | None = Field(
        description="Nome del pianeta di riferimento.", default=None
    )
    max_distance: int | None = Field(
        description="La distanza massima dal pianeta di riferimento.", default=None
    )


# endregion

# region Cypher Agent response


class CypherAgentResponse(BaseModel):
    dishes: list[Dish] | None = Field(
        description="La lista dei piatti che soddisfano la query dell'utente. Usato per la risposta finale.",
        default_factory=list,
    )


# endregion


class CSVEntry(BaseModel):
    question_id: int = Field(description="The row_id of the question of the user.")
    result: str = Field(
        description="The result of the user query as a list of id, separated by a comma."
    )
