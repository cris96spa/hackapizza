from langchain_core.runnables import RunnableSequence
from hackathon.session import SessionManager
from langchain.prompts import ChatPromptTemplate
from hackathon.graph.models import KnowledgeEnrichmentResponse
from hackathon.graph.prompts import DECIDE_KNOWLEDGE_ENRICHMENT_PROMPT

llm = SessionManager().model_manager.model
structured_llm_generator = llm.with_structured_output(KnowledgeEnrichmentResponse)

generation_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", DECIDE_KNOWLEDGE_ENRICHMENT_PROMPT),
        (
            "human",
            "User query: \n\n {question}",
        ),
    ]
)

generator: RunnableSequence = generation_prompt | structured_llm_generator  # type: ignore
