from langchain_core.prompts import ChatPromptTemplate
from hackathon.session import SessionManager
from hackathon.graph.models import RouteQuery
from hackathon.graph.prompts import ROUTER_PROMPT

llm = SessionManager().model_manager.model
structured_llm_router = llm.with_structured_output(RouteQuery)


route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", ROUTER_PROMPT),
        ("human", "{question}"),
    ]
)

question_router = route_prompt | structured_llm_router
