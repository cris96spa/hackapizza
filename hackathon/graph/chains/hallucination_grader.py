from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from hackathon.session import SessionManager
from hackathon.graph.models import GradeHallucinations
from hackathon.graph.prompts import HALLUCINATION_GRADER_PROMPT

llm = SessionManager().model_manager.model
structured_llm_grader = llm.with_structured_output(GradeHallucinations)


hallucination_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", HALLUCINATION_GRADER_PROMPT),
        (
            "human",
            "Set of facts: \n\n {documents} \n\n LLM generation: {generation}",
        ),
    ]
)

hallucination_grader: RunnableSequence = hallucination_prompt | structured_llm_grader  # type: ignore
