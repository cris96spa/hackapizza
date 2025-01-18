import os
from langchain_text_splitters import MarkdownHeaderTextSplitter
import pymupdf4llm
from langchain_core.documents import Document


class MenuIngestor:
    """
    Ingests documents from menu folder.

    Parameters
    ----------
    path : str
        Path to the menu folder.
    """

    def __init__(self):
        headers_to_split_on = [("#", "header_1"), ("##", "header_2")]
        self.markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)

    def ingest(self, file_path: str) -> list[Document]:
        # Obtain file name from path
        file_name = os.path.basename(file_path)

        md_text = pymupdf4llm.to_markdown(file_path)
        split_docs = self.markdown_splitter.split_text(md_text)

        # Add filename to metadata
        for doc in split_docs:
            doc.metadata["source"] = file_name

        return split_docs
