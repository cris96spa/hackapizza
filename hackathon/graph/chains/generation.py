from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from hackathon.session_manager import SessionManager

llm = SessionManager().model_manager.model

prompt = hub.pull("rlm/rag-prompt")

generation_chain = prompt | llm | StrOutputParser()
