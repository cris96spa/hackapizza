from langchain.schema import Document


class Formatter:
    @staticmethod
    def format_document(document: Document) -> str:
        """
        Formats a document to be displayed in the prompt
        """

        formatted_document = f"Metadata: {document.metadata}\n"
        formatted_document += f"Text: {document.page_content}\n"

        return formatted_document

    @staticmethod
    def format_documents(documents: list[Document]) -> str:
        """
        Formats a list of documents to be displayed in the prompt
        """

        formatted_documents = ""
        for document in documents:
            formatted_documents += Formatter.format_document(document)
            formatted_documents += "\n"

        return formatted_documents
