from langchain_ibm import WatsonxEmbeddings
import os
from os import listdir
from os.path import isfile, join
from hackathon.enums import LLMProvider
from hackathon.utils.formatter import Formatter
from hackathon.utils.settings.settings_provider import SettingsProvider
from langchain.text_splitter import RecursiveCharacterTextSplitter
from hackathon.models import menu_metadata_keys, dish_metadata_keys
from hackathon.ingestion.menu import MenuIngestor
from hackathon.graph.chains.ingestion_metadata_extractor import (
    menu_metadata_extractor,
    dish_metadata_extractor,
)
from hackathon.ingestion.cooking_manual import CookingManualIngestor
from hackathon.ingestion.galactic_code import GalacticCodeIngestor
from hackathon.graph.prompts import (
    MENU_METADATA_LICENSES_PROMPT,
    DISHES_METADATA_INGREDIENTS_PROMPT,
)

from langchain_chroma.vectorstores import Chroma
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
import numpy as np

from tqdm import tqdm
import torch
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorstoreManager:
    def __init__(self):
        self._embeddings = None
        self._vectorstore = None
        self._retriever = None
        self.settings_provider = SettingsProvider()
        self._current_key_values_metadata = None

    def _setup_vectorstore(self):
        # Setup the vectorstore
        logger.info("Initializing vectorstore...")

        # Setup the torch device
        device = "cpu"
        if torch.cuda.is_available():
            device = "cuda"
        elif torch.backends.mps.is_available():
            device = "mps"

        # Setup the model for embeddings
        model_kwargs = {"device": device}
        encode_kwargs = {"normalize_embeddings": False}

        if self.settings_provider.get_embeddings_provider() == LLMProvider.HUGGINGFACE:
            self._embeddings = HuggingFaceEmbeddings(
                model_name=self.settings_provider.get_embeddings_model_name(),
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs,
            )
        elif self.settings_provider.get_embeddings_provider() == LLMProvider.IBM:
            self._embeddings = WatsonxEmbeddings(
                model_id=self.settings_provider.get_embeddings_model_name(),  # type: ignore
                url=self.settings_provider.get_ibm_endpoint_url(),  # type: ignore
                project_id=self.settings_provider.get_ibm_project_id(),  # type: ignore
            )
        elif self.settings_provider.get_embeddings_provider() == LLMProvider.OPEN_AI:
            self._embeddings = OpenAIEmbeddings(
                model=self.settings_provider.get_embeddings_model_name(),
                # With the `text-embedding-3` class
                # of models, you can specify the size
                # of the embeddings you want returned.
                # dimensions=1024
            )
        else:
            raise ValueError(
                f"Unsupported embeddings provider: {self.settings_provider.get_embeddings_provider()}"
            )

        # Try to load the FAISS vectorstore

        try:
            self._vectorstore = FAISS.load_local(
                self.settings_provider.get_vectorstore_path(),
                self._embeddings,
                allow_dangerous_deserialization=True,
            )
        except RuntimeError:
            logger.info("FAISS vectorstore not found. Loading it")
            self._load_knowledge_base()

        logger.info("Vectorstore initialized successfully.")

        self._retriever = self._vectorstore.as_retriever(
            search_kwargs={"k": 12, "fetch_k": self._vectorstore.index.ntotal}
        )

    @property
    def embeddings(self) -> Embeddings:
        if not self._embeddings:
            self._setup_vectorstore()
        return self._embeddings  # type: ignore

    @property
    def vectorstore(self) -> VectorStore:
        if not self._vectorstore:
            self._setup_vectorstore()
        return self._vectorstore  # type: ignore

    @property
    def retriever(self) -> VectorStoreRetriever:
        if not self._retriever:
            self._setup_vectorstore()
        return self._retriever  # type: ignore

    @property
    def current_key_values_metadata(self) -> VectorStoreRetriever:
        if not self._current_key_values_metadata:
            self._setup_vectorstore()
            self._current_key_values_metadata = self.get_current_key_values_metadata()
        return self._current_key_values_metadata  # type: ignore

    def _load_knowledge_base(self, dir_path: str | None = None):
        """Load knowledge base from a directory into the vectorstore.

        Args:
            directory_path: The path to the directory containing the knowledge base.
                If None, the default knowledge base directory is used.

        """

        # Load the source of truth documents
        source_of_truth_docs = self._load_source_of_truth()
        menus_docs = self._load_menus()

        docs = source_of_truth_docs + menus_docs

        self._vectorstore = FAISS.from_documents(
            documents=docs,
            embedding=self._embeddings,
        )

        self._vectorstore.save_local(
            folder_path=self.settings_provider.get_vectorstore_path()
        )

    def is_document_in_vectorstore(self, document: Document) -> bool:
        """Check if a document is already in the vectorstore.

        Args:
            document: The document to check.

        Returns:
            True if the document is in the vectorstore, False otherwise.
        """
        query_results = self.vectorstore.similarity_search(
            document.page_content,
            k=1,
        )
        return query_results == document

    def add_document(self, document: Document):
        """Add a document to the vectorstore.

        Args:
            document: The document to add.
        """
        if self.is_document_in_vectorstore(document):
            return

        self.vectorstore.add_texts(
            texts=[document.page_content],
            metadatas=[document.metadata],
        )

    def add_documents(self, documents: list[Document]):
        """Add a list of documents to the vectorstore.

        Args:
            documents: The list of documents to add.
        """
        for doc in tqdm(documents, desc="Adding documents to vectorstore"):
            self.add_document(doc)

    def _load_source_of_truth(self) -> list[Document]:
        galactic_code_documents = GalacticCodeIngestor().ingest(
            self.settings_provider.get_galactic_code_path()
        )

        for doc in tqdm(
            galactic_code_documents,
            desc="Adding galactic code documents to vectorstore",
        ):
            doc.metadata.update({"is_code": True})
            doc.page_content = Formatter.format_document(doc)

        cooking_manual_documents = CookingManualIngestor().ingest(
            self.settings_provider.get_cooking_manual_path()
        )

        for doc in tqdm(
            cooking_manual_documents,
            desc="Adding cooking manual documents to vectorstore",
        ):
            doc.metadata.update({"is_manual": True})
            doc.page_content = Formatter.format_document(doc)

        documents = galactic_code_documents + cooking_manual_documents

        return documents

    def _load_menus(self) -> list[Document]:
        menu_path = self.settings_provider.get_menu_path()

        if not os.path.exists(menu_path):
            raise FileNotFoundError(f"Menu file not found at path: {menu_path}")

        # Load the menu documents
        menu_file_names = [
            file for file in listdir(menu_path) if isfile(join(menu_path, file))
        ]

        # Define the menu ingestor
        menu_ingestor = MenuIngestor()

        documents = []
        menu_metadata_values = {key: set() for key in menu_metadata_keys}
        dish_metadata_values = {key: set() for key in dish_metadata_keys}

        # Scan the menu files
        for menu in tqdm(menu_file_names, desc="Adding menu documents to vectorstore"):
            # Load all chunks of the given menu
            menu_splits = menu_ingestor.ingest(os.path.join(menu_path, menu))

            # Take the first chunk as the header
            menu_header = menu_splits[0]

            # call llm to extract metadata
            meta = ""
            for key in menu_metadata_keys:
                meta += f"{key}: {', '.join(menu_metadata_values[key])}\n"

            header_metadata = menu_metadata_extractor.invoke(
                {
                    "document": menu_header,
                    "metadata": meta,
                    "context": MENU_METADATA_LICENSES_PROMPT,
                }
            )

            # Convert the structured output to dict
            header_metadata = header_metadata.model_dump()
            header_metadata["restaurant_name"] = menu.split(".")[0].lower()

            for key in menu_metadata_keys:
                if key in header_metadata:
                    if isinstance(header_metadata[key], list):
                        for value in header_metadata[key]:
                            menu_metadata_values[key].add(value)
                    elif isinstance(header_metadata[key], str):
                        menu_metadata_values[key].add(header_metadata[key])

            # Add each document chunk to the vector store
            for i, chunk in enumerate(menu_splits):
                if i > 0:
                    meta = ""
                    for key in dish_metadata_keys:
                        meta += f"{key}: {', '.join(dish_metadata_values[key])}\n"

                    dish_metadata = dish_metadata_extractor.invoke(
                        {
                            "document": chunk,
                            "metadata": meta,
                            "context": DISHES_METADATA_INGREDIENTS_PROMPT,
                        }
                    )
                    dish_metadata = dish_metadata.model_dump()

                    recursive_splitter = (
                        RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                            chunk_size=256, chunk_overlap=0
                        )
                    )
                    splits = recursive_splitter.split_documents(chunk)
                    for split in splits:
                        split.metadata.update(dish_metadata)

                        for key in dish_metadata_keys:
                            if key in dish_metadata:
                                if isinstance(dish_metadata[key], list):
                                    for value in dish_metadata[key]:
                                        dish_metadata_values[key].add(value)
                                elif isinstance(dish_metadata[key], str):
                                    dish_metadata_values[key].add(dish_metadata[key])

                    split.page_content = Formatter.format_document(split)
                    split.metadata.update(header_metadata)
                    documents.append(split)

        return documents

    def get_current_key_values_metadata(self) -> dict[str, set[str]]:
        """Get the current key values metadata in the vectorstore.

        Returns:
            A dictionary containing the current key values metadata in the vectorstore.
        """
        embedding_dim = self.vectorstore.index.d
        dummy_vector = np.zeros(embedding_dim)

        # Retrieve all documents by setting k to the total number of documents
        docs_and_scores = self.vectorstore.similarity_search_with_score_by_vector(
            dummy_vector, k=self.vectorstore.index.ntotal
        )

        key_values_metadata = {}

        for doc_and_score in docs_and_scores:
            document = doc_and_score[0]

            for key, value in document.metadata.items():
                if key == "is_code" or key == "is_manual" or value is None:
                    continue
                if key not in key_values_metadata:
                    key_values_metadata[key] = set()
                if isinstance(value, list):
                    for v in value:
                        key_values_metadata[key].add(v)
                else:
                    # Add value
                    key_values_metadata[key].add(value)

        return key_values_metadata


if __name__ == "__main__":
    import os

    print(os.getcwd())
    from dotenv import load_dotenv

    load_dotenv()
    vm = VectorstoreManager()
    vm._setup_vectorstore()

    assert vm.vectorstore is not None
