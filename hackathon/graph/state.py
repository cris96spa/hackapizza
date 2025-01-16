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

    question: str = Field(
        description='The question asked by the user.', default=''
    )
    generation: str = Field(description='The LLM generation.', default='')
    web_search: bool = Field(
        description='Whether to include web search in the response.',
        default=False,
    )
    documents: list[Document] = Field(
        description='The list of documents.', default_factory=list
    )
