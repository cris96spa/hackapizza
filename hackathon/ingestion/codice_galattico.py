import os
from langchain_core.documents import Document
import re
from langchain_core.prompts import PromptTemplate
from hackathon.session import SessionManager
from markitdown import MarkItDown


from pydantic import BaseModel, Field


class SplitHeaders(BaseModel):
    headers: list[str] = Field(description="List of headers to split the document on")


class CodiceGalatticoIngestor:
    """
    Ingests documents from Codice Galattico.
    """

    def __init__(self):
        split_prompt_template = "Given this markdown document, provide a list of headers of the document to split the document on, keep only level 1 header (e.g. 1 Definizioni, 2 Sostanze regolamentate), include eventual appendix. \nDocument:\n\n{document}\n\n"
        split_prompt = PromptTemplate.from_template(split_prompt_template)
        llm = SessionManager().model_manager.model
        structured_llm = llm.with_structured_output(SplitHeaders)
        self.split_chain = split_prompt | structured_llm
        self.markitdown = MarkItDown()

    def ingest(self, file_path: str) -> list[Document]:
        """
        Ingests a document from a file path.
        """
        # Obtain file name from path
        file_name = os.path.basename(file_path)

        result = self.markitdown.convert(file_path)
        md_text = result.text_content

        split_headers = self.split_chain.invoke({"document": md_text})

        split_text = self._split_markdown_by_headers(md_text, split_headers.headers)

        documents = []
        for header, text in split_text.items():
            documents.append(
                Document(text, metadata={"header": header, "source": file_name})
            )

        return documents

    def _split_markdown_by_headers(
        self, markdown_text: str, headers: list[str]
    ) -> dict:
        """
        Splits a markdown text into sections based on a list of headers.
        Includes any text before the first header as a "preamble."

        Args:
            markdown_text (str): The markdown text to be split.
            headers (list of str): A list of header strings to use as delimiters.

        Returns:
            dict: A dictionary where keys are headers and values are the corresponding section content.
                Includes a "_preamble_" key for text before the first header.
        """
        # Create a regular expression to match headers
        header_pattern = "|".join(re.escape(f"{header}") for header in headers)

        # Split the markdown text by headers
        sections = re.split(f"({header_pattern})", markdown_text)

        # Pair headers with their respective content
        result = {"Introduction": ""}
        current_header = "Introduction"
        for section in sections:
            section = section.strip()
            if section in [f"{header}" for header in headers]:
                current_header = section
                result[current_header] = ""
            elif current_header:
                result[current_header] += section

        return result
