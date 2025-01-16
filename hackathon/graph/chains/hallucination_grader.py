from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from hackathon.session_manager import SessionManager
from hackathon.graph.models import GradeHallucinations

llm = SessionManager().model_manager.model
structured_llm_grader = llm.with_structured_output(GradeHallucinations)

system = """You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts. \n 
     Give a binary score True or False. True means that the answer is grounded in / supported by the set of facts."""

hallucination_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        (
            "human",
            "Set of facts: \n\n {documents} \n\n LLM generation: {generation}",
        ),
    ]
)

hallucination_grader: RunnableSequence = hallucination_prompt | structured_llm_grader  # type: ignore
