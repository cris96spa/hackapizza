from pydantic import BaseModel, Field
from typing import Literal
from langchain.schema import Document


# region Grade Documents
class GradeDocuments(BaseModel):
    """Valutazione binaria per la rilevanza dei documenti alla domanda."""

    binary_score: bool = Field(
        description="Il documento è rilevante per la domanda? True o False"
    )


# endregion


# Entry for CSV
class CSVEntry(BaseModel):
    question_id: int = Field(description="The row_id of the question of the user.")
    result: str = Field(
        description="The result of the user query as a list of id, separated by a comma."
    )


# endregion


# Generation Response
class GenerationResponse(BaseModel):
    dishes: list[str] = Field(
        description="The list of dishes compliant with the user query."
    )


class KnowledgeEnrichmentResponse(BaseModel):
    """Response for the knowledge enrichment task."""

    need_document: bool = Field(
        description="True se è necessario consultare questa knowledge source, False altrimenti."
    )


class Planet(BaseModel):
    name: str = Field(description="The name of the planed.")
    distance: int = Field(description="The distance from the planet.")


# Planet Distance Response
class PlanetDistanceResponse(BaseModel):
    planets: list[str] = Field(
        description="The list of planets close enough to the specified planet."
    )
