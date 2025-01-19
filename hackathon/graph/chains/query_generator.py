from langchain_core.prompts import ChatPromptTemplate
from hackathon.session import SessionManager
from hackathon.graph.models import GradeDocuments
from langchain_core.runnables import RunnableSequence
from hackathon.graph.prompts import QUERY_GENERATION_PROMPT
from langchain_core.output_parsers.json import JsonOutputParser

llm = SessionManager().model_manager.model

parser = JsonOutputParser()

from langchain_core.output_parsers.json import JsonOutputParser
query_generation_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", QUERY_GENERATION_PROMPT),
        (
            "human",
            "Domanda dell'utente: {question}",
        ),
    ]
)

query_generator: RunnableSequence = query_generation_prompt | llm | parser  # type: ignore