from pydantic import BaseModel, Field
from typing import Literal


# region Grade Documents
class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: bool = Field(
        description='Documents are relevant to the question, True or False'
    )


# endregion


# region Grade Hallucinations
class GradeHallucinations(BaseModel):
    """Binary score for hallucination present in generation answer."""

    binary_score: bool = Field(
        description='Answer is grounded in the facts, True or False'
    )


# endregion


# region Grade Answer
class GradeAnswer(BaseModel):
    binary_score: bool = Field(
        description='Answer addresses the question, True or False'
    )


# endregion

# region Router


class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal['vectorstore', 'websearch'] = Field(
        description='Given a user question choose to route it to web search or a vectorstore.',
    )


# endregion
