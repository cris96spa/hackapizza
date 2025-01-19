from pydantic import BaseModel, Field
from langchain.schema import Document
from hackathon.models import MenuMetadata, DishMetadata


class GraphState(BaseModel):
    """
    Represents the state of our graph.

    Attributes:
        question: The question asked by the user.
        question_id: The id of the user's question.
        generation: The LLM generation.
        documents: The list of documents.
        dishes: The list of dishes.
        menu_metadata: The metadata that describes menu elements.
    """

    question: str = Field(description="The question asked by the user.", default="")
    question_id: int = Field(description="The id of the user's question.", default=0)
    documents: list[Document] = Field(
        description="The list of documents.", default_factory=list
    )
    dishes: list[str] = Field(description="The list of dishes.", default_factory=list)
    menu_metadata: MenuMetadata | None = Field(
        description="The metadata describing menu elements.", default=None
    )
    dish_metadata: DishMetadata | None = Field(
        description="The metadata describing dishes.", default=None
    )
