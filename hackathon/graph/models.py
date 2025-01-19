from pydantic import BaseModel, Field
from typing import Literal
from langchain.schema import Document

# region Router


class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["vectorstore", "websearch"] = Field(
        description="Given a user question choose to route it to web search or a vectorstore.",
    )


# endregion


# region Grade Documents
class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: bool = Field(
        description="Documents are relevant to the question, True or False"
    )


# endregion


# region Grade Hallucinations
class GradeHallucinations(BaseModel):
    """Binary score for hallucination present in generation answer."""

    binary_score: bool = Field(
        description="Answer is grounded in the facts, True or False"
    )


# endregion


# region Grade Answer
class GradeAnswer(BaseModel):
    binary_score: bool = Field(
        description="Answer addresses the question, True or False"
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


class Planet(BaseModel):
    name: str = Field(description="The name of the planed.")
    distance: int = Field(description="The distance from the planet.")


# Planet Distance Response
class PlanetDistanceResponse(BaseModel):
    planets: list[str] = Field(
        description="The list of planets close enough to the specified planet."
    )
