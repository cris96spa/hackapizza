from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from hackathon.managers.model_manager import ModelManager
from hackathon.graph.prompts import QUERY_METADATA_EXTRACTION_PROMPT
from hackathon.models import MenuMetadata, DishMetadata

llm = ModelManager().model
stuctured_llm_menu_metadata_extract = llm.with_structured_output(MenuMetadata)
stuctured_llm_dish_metadata_extract = llm.with_structured_output(DishMetadata)

menu_metadata_promt = ChatPromptTemplate.from_messages(
    [
        ("system", QUERY_METADATA_EXTRACTION_PROMPT),
        (
            "human",
            """Estrai i metadati da questo documento: {document}
            """,
        ),
    ]
)

menu_metadata_extractor: RunnableSequence = (
    menu_metadata_promt | stuctured_llm_menu_metadata_extract
)  # type: ignore


dish_metadata_extractor: RunnableSequence = (
    menu_metadata_promt | stuctured_llm_dish_metadata_extract
)  # type: ignore
