import os
from langchain_text_splitters import MarkdownHeaderTextSplitter
import pymupdf4llm
from langchain_core.documents import Document


class MenuIngestor:
    """
    Ingests documents from menu folder.
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
            if "header_1" in doc.metadata:
                doc.page_content = doc.metadata["header_1"] + doc.page_content
            if "header_2" in doc.metadata:
                doc.page_content = doc.metadata["header_2"] + doc.page_content

        return split_docs
