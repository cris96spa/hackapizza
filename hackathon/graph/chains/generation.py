from langchain_core.runnables import RunnableSequence
from hackathon.graph.models import GenerationResponse
from hackathon.session import SessionManager
from langchain.prompts import ChatPromptTemplate
from hackathon.graph.prompts import GENERATION_PROMPT

llm = SessionManager().model_manager.model
structured_llm_generator = llm.with_structured_output(GenerationResponse)

generation_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", GENERATION_PROMPT),
        (
            "human",
            "User query: \n\n {question} \n\n Context: {documents}",
        ),
    ]
)

generator: RunnableSequence = generation_prompt | structured_llm_generator  # type: ignore
