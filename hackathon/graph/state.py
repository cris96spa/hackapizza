from pydantic import BaseModel, Field
from langchain.schema import Document


class GraphState(BaseModel):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        web_search: whether to add search
        documents: list of documents
    """

    question: str = Field(description="The question asked by the user.", default="")
    documents: list[Document] = Field(
        description="The list of documents.", default_factory=list
    )
    dishes: list[str] = Field(description="The list of dishes.", default_factory=list)
