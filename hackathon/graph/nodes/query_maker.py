import logging
from typing import Any, Callable, Dict
from hackathon.graph.state import GraphState
from hackathon.models import DishMetadata, MenuMetadata
from hackathon.session import SessionManager
from hackathon.graph.chains.query_generator import query_generator
from langchain.schema import Document

mongo_db_store_manager = SessionManager().mongo_db_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def query_maker(state: GraphState) -> Dict[str, Any]:
    """
    Retrieve documents from the vector store.

    Args:
        state: The current state of the graph.

    Returns:
        A dictionary containing the retrieved documents.
    """
    mongo_possible_values = mongo_db_store_manager.describe_collection()
    max_tries = 3
    error = None
    empty_result = False
    documents = []
    previous_query_prompt = ""

    for tentative in range(max_tries):
        try:
            if error is None and not empty_result:
                # Generate a query without any error context.
                query = query_generator.invoke(
                    {
                        "question": state.question,
                        "mongo_possible_values": mongo_possible_values,
                        "previous_query_prompt": previous_query_prompt,
                    }
                )
            else:
                # Update the prompt with error or empty result context.
                if error is not None:
                    previous_query_prompt += f"\nThe previous query '{query}' caused an error: {error}. Please provide a valid query."
                if empty_result:
                    previous_query_prompt += f"\nThe previous query '{query}' returned 0 results. Please provide a new query."

                query = query_generator.invoke(
                    {
                        "question": state.question,
                        "mongo_possible_values": mongo_possible_values,
                        "previous_query_prompt": previous_query_prompt,
                    }
                )

            print(f"Generated Query: {query}")

            # Attempt to retrieve documents.
            documents = mongo_db_store_manager.collection.find(query)
            documents = list(documents)

            if not documents:
                empty_result = True
                print("No documents found. Retrying...")
                continue

            print(f"Retrieved {len(documents)} documents")
            break

        except Exception as e:
            error = e
            print(
                f"Error during retrieval or query generation: {e} (Attempt {tentative + 1}/{max_tries})"
            )

    # Construct LangChain Document objects.
    langchain_documents = []
    for document in documents:
        # Remove the embedding key if present.
        document.pop("embedding", None)

        page_content = document.pop("page_content", "")
        metadata = document
        metadata.pop("_id")

        langchain_document = Document(page_content=page_content, metadata=metadata)
        langchain_documents.append(langchain_document)

    if not documents:
        print("Failed to retrieve documents after maximum retries.")
        print("Falling back to vector store")

    return {"documents": langchain_documents[:15]}
