from langchain_core.output_parsers import StrOutputParser
from hackathon.session import SessionManager
from langchain.prompts import ChatPromptTemplate
from hackathon.graph.prompts import GENERATION_PROMPT

llm = SessionManager().model_manager.model

prompt = ChatPromptTemplate.from_template(GENERATION_PROMPT)

generation_chain = prompt | llm | StrOutputParser()
