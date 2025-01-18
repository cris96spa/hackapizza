from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from hackathon.managers.model_manager import ModelManager
from hackathon.ingestion.prompts import METADATA_EXTRACTION_PROMPT
from hackathon.models import MenuMetadata

llm = ModelManager().model
stuctured_llm_metadata_extract = llm.with_structured_output(MenuMetadata)


menu_metadata_promt = ChatPromptTemplate.from_messages(
    [
        ("system", METADATA_EXTRACTION_PROMPT),
        (
            "human",
            "Extract the metadata from this document: {document}",
        ),
    ]
)

menu_metadata_extractor: RunnableSequence = (
    menu_metadata_promt | stuctured_llm_metadata_extract
)  # type: ignore
