from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from hackathon.session_manager import SessionManager
from hackathon.graph.models import GradeAnswer

llm = SessionManager().model_manager.model
structured_llm_grader = llm.with_structured_output(GradeAnswer)

system = """You are a grader assessing whether an answer addresses / resolves a question \n 
     Give a binary score True or False. True means that the answer resolves the question."""

answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        (
            "human",
            "User question: \n\n {question} \n\n LLM generation: {generation}",
        ),
    ]
)

answer_grader: RunnableSequence = answer_prompt | structured_llm_grader  # type: ignore
