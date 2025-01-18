from typing import Any, Dict

from langchain.schema import Document
from langchain_community.tools.tavily_search import TavilySearchResults

from hackathon.graph.state import GraphState

web_search_tool = TavilySearchResults(max_results=3)


def web_search(state: GraphState) -> Dict[str, Any]:
    print("---WEB SEARCH---")
    question = state.question
    documents = state.documents

    docs = web_search_tool.invoke({"query": question})

    web_results = "\n".join([d["content"] for d in docs])
    web_results_doc = Document(page_content=web_results)

    if documents is not None:
        documents.append(web_results_doc)
    else:
        documents = [web_results_doc]
    return {"documents": documents, "question": question}
