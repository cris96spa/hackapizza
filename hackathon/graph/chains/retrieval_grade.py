from langchain_core.prompts import ChatPromptTemplate
from hackathon.session import SessionManager
from hackathon.graph.models import GradeDocuments
from hackathon.graph.prompts import RETRIEVAL_GRADER_PROMPT

llm = SessionManager().model_manager.model


structured_llm_grader = llm.with_structured_output(GradeDocuments)

grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", RETRIEVAL_GRADER_PROMPT),
        (
            "human",
            "Documento: \n\n {document} \n\n Domanda dell'utente: {question}",
        ),
    ]
)

retrieval_grader = grade_prompt | structured_llm_grader
