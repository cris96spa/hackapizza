from langchain_core.prompts import ChatPromptTemplate
from hackathon.session_manager import SessionManager
from hackathon.graph.models import GradeDocuments

llm = SessionManager().model_manager.model


structured_llm_grader = llm.with_structured_output(GradeDocuments)

system = """You are a grader assessing relevance of a retrieved document to a user question. \n 
    If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant. \n
    Give a binary score True or False score to indicate whether the document is relevant to the question."""
grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        (
            "human",
            "Retrieved document: \n\n {document} \n\n User question: {question}",
        ),
    ]
)

retrieval_grader = grade_prompt | structured_llm_grader
