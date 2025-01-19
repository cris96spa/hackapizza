import logging
from typing import Any, Callable, Dict
from hackathon.graph.state import GraphState
from hackathon.models import DishMetadata, MenuMetadata
from hackathon.session import SessionManager

retriever = SessionManager().vectorstore_manager.retriever

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_string(string: str):
    return string.lower().replace("_", " ").replace("'", " ")


# def condition(s1: str, s2: str) -> bool:
#     return s1 in s2


def condition(s1: str, s2: str) -> bool:
    """Check that at least 80% of the words overlap"""

    s1 = s1.split()
    s2 = s2.split()

    if len(s1) == 0 or len(s2) == 0:
        return False

    common_letters = set(s1).intersection(s2)
    return len(common_letters) / len(s1) > 0.8 or len(common_letters) / len(s2) > 0.8


def search_string_in_dict(string: str, key: str, dictionary: dict):
    search_string = clean_string(string)

    if key not in dictionary:
        return False

    if dictionary[key] is None:
        return True

    if isinstance(dictionary[key], str):
        return condition(search_string, clean_string(dictionary[key]))

    elif isinstance(dictionary[key], list):
        return any(condition(search_string, clean_string(x)) for x in dictionary[key])

    else:
        raise ValueError(f"Unsupported type {type(dictionary[key])}")


def filter_with_menu_metadata(metadata: MenuMetadata):
    conditions = []
    fields = []

    if metadata.chef_name is not None:
        fields.append("chef_name")
        conditions.append(
            lambda doc_metadata: search_string_in_dict(
                string=metadata.chef_name, key="chef_name", dictionary=doc_metadata
            )
        )

    if metadata.restaurant_name is not None:
        fields.append("restaurant_name")
        conditions.append(
            lambda doc_metadata: search_string_in_dict(
                string=metadata.restaurant_name,
                key="restaurant_name",
                dictionary=doc_metadata,
            )
        )

    if metadata.planet_name is not None:
        fields.append("planet_name")
        conditions.append(
            lambda doc_metadata: search_string_in_dict(
                string=metadata.planet_name, key="planet_name", dictionary=doc_metadata
            )
        )

    if metadata.licences is not None and len(metadata.licences) > 0:
        fields.append("licences")
        conditions.append(
            lambda doc_metadata: any(
                search_string_in_dict(
                    string=lic, key="licences", dictionary=doc_metadata
                )
                for lic in metadata.licences
            )
        )

    if len(conditions) == 0:
        print("No metadata fields to filter")
        filter_fn = None

    else:
        print(f"Filtering documents with metadata fields: {fields}")
        filter_fn = lambda x: any(cond(x) for cond in conditions)  # noqa

    return filter_fn


def filter_with_dish_metadata(metadata: DishMetadata):
    conditions = []
    fields = []

    if metadata.dish_name is not None:
        fields.append("dish_name")
        conditions.append(
            lambda doc_metadata: search_string_in_dict(
                string=metadata.dish_name, key="dish_name", dictionary=doc_metadata
            )
        )

    if metadata.dish_techniques is not None and len(metadata.dish_techniques):
        fields.append("dish_techniques")
        conditions.append(
            lambda doc_metadata: any(
                search_string_in_dict(
                    string=tech, key="dish_techniques", dictionary=doc_metadata
                )
                for tech in metadata.dish_techniques
            )
        )

    if metadata.dish_ingredients is not None and len(metadata.dish_ingredients):
        fields.append("dish_ingredients")
        conditions.append(
            lambda doc_metadata: any(
                search_string_in_dict(
                    string=ing, key="dish_ingredients", dictionary=doc_metadata
                )
                for ing in metadata.dish_ingredients
            )
        )

    if len(conditions) == 0:
        logger.info("No metadata fields to filter")
        filter_fn = None

    else:
        logger.info(f"Filtering documents with metadata fields: {fields}")
        filter_fn = lambda x: any(cond(x) for cond in conditions)  # noqa

    return filter_fn


def retrieve(state: GraphState) -> Dict[str, Any]:
    """
    Retrieve documents from the vector store.

    Args:
        state: The current state of the graph.

    Returns:
        A dictionary containing the retrieved documents.
    """

    meta_filter_fn = None
    dish_filter_fn = None

    if state.menu_metadata is not None:
        meta_filter_fn = filter_with_menu_metadata(state.menu_metadata)

    if state.dish_metadata is not None:
        dish_filter_fn = filter_with_dish_metadata(state.dish_metadata)

    filter_fn = None
    if meta_filter_fn is not None:
        if dish_filter_fn is not None:
            filter_fn = lambda x: meta_filter_fn(x) or dish_filter_fn(x)  # noqa
        else:
            filter_fn = meta_filter_fn
    else:
        if dish_filter_fn is not None:
            filter_fn = dish_filter_fn

    documents = retriever.invoke(
        state.question,
        search_kwargs={
            "k": 6,
            "fetch_k": SessionManager().vectorstore_manager._vectorstore.index.ntotal,
        },
        filter=filter_fn,
    )

    # documents = retriever.invoke(state.question, filter_fn=filter_fn)
    return {"documents": documents}
