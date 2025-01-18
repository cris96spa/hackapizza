from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from hackathon.session import SessionManager
from hackathon.graph.models import GradeAnswer
from hackathon.graph.prompts import ANSWER_GRADER_PROMPT

llm = SessionManager().model_manager.model
structured_llm_grader = llm.with_structured_output(GradeAnswer)


answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", ANSWER_GRADER_PROMPT),
        (
            "human",
            "User question: \n\n {question} \n\n LLM generation: {generation}",
        ),
    ]
)

answer_grader: RunnableSequence = answer_prompt | structured_llm_grader  # type: ignore
