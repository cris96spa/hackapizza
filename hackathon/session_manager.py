import os
from typing import Any

from dotenv import load_dotenv
from langchain_chroma.vectorstores import Chroma
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyMuPDFLoader,
    Docx2txtLoader,
    TextLoader,
)
from hackathon.graph.models import ModelResponse
from langchain_core.runnables import RunnableSerializable
from tqdm import tqdm
import torch
import logging
import polars as pl
import time

# Load environment variables
load_dotenv()

# Constants
DATA_PATH = "data"
VECTORSTORE_PATH = os.path.join(DATA_PATH, "vectorstore")
KNOWLEDGE_BASE_PATH = os.path.join(DATA_PATH, "knowledge")
DATASET_PATH = os.path.join(DATA_PATH, "evaluation_dataset.csv")
EMBEDDINGS_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
# EMBEDDINGS_MODEL_NAME = "intfloat/multilingual-e5-large-instruct"
# EMBEDDINGS_MODEL_NAME = 'answerdotai/ModernBERT-base'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Singleton(type):
    _instances: dict[type[Any], Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


# region VectorstoreManager
class VectorstoreManager(metaclass=Singleton):
    def __init__(self):
        self._embeddings = None
        self._vectorstore = None
        self._retriever = None

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

        self._embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDINGS_MODEL_NAME,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
        )

        # Initialize the vectorstore
        self._vectorstore = Chroma(
            embedding_function=self._embeddings,
            persist_directory=VECTORSTORE_PATH,
        )

        # Check if the knowledge base must be loaded
        # to avoid loading it multiple times
        if len(self.vectorstore.get()["documents"]) == 0:  # type: ignore
            logger.info(f"Loading the knowledge base {KNOWLEDGE_BASE_PATH}")
            self._load_knowledge_base()
        else:
            logger.info("Knowledge base already loaded. Skipping...")

        logger.info("Vectorstore initialized successfully.")

        # Setup the retriever
        self._retriever = self._vectorstore.as_retriever(search_kwargs={"k": 5})

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

    def _load_knowledge_base(self, directory_path: str | None = None):
        """Load knowledge base from a directory into the vectorstore.

        Args:
            directory_path: The path to the directory containing the knowledge base.
                If None, the default knowledge base directory is used.

        """
        if not directory_path:
            directory_path = KNOWLEDGE_BASE_PATH

        if not os.path.exists(directory_path):
            logger.warning(
                f"Directory {directory_path} does not exist. Skipping file loading."
            )
            return

        logger.info(f"Loading knowledge base from directory: {directory_path}")

        # Supported file loaders
        type_loaders_mapping = {
            ".pdf": PyMuPDFLoader,
            ".docx": Docx2txtLoader,
            ".txt": TextLoader,
        }

        documents = []
        for _type, cls in type_loaders_mapping.items():
            # Load knowledge_base from the directory
            loader = DirectoryLoader(
                directory_path,
                glob=f"**/*{_type}",
                loader_cls=cls,
            )
            documents.extend(loader.load())

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=20)
        split_docs = text_splitter.split_documents(documents)

        # Add documents to the vectorstore
        self.add_documents(split_docs)

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


# endregion


# region ModelManager
class ModelManager(metaclass=Singleton):
    def __init__(self):
        self._model = None

    def _setup_model(self):
        # Configure the model_name with environment variables and settings
        model_name = os.getenv("MODEL_NAME", "gpt-4o")
        temperature = float(os.getenv("MODEL_TEMPERATURE", "0.0"))

        # Initialize ChatOpenAI instance
        self._model = ChatOpenAI(model=model_name, temperature=temperature)

    @property
    def model(self) -> BaseChatModel:
        if not self._model:
            self._setup_model()
        return self._model  # type: ignore


# endregion


# region DatasetManager
class DatasetManager(metaclass=Singleton):
    """Singleton class for managing the dataset containing the interactions with the
    RAG system.
    """

    def __init__(self):
        self._dataset = None
        self._dataset_path = None

    def _setup_dataset(self):
        """Setup the dataset by loading the CSV file containing the interactions with the
        RAG system.
        """

        self._dataset_path = DATASET_PATH
        try:
            self._dataset = pl.read_csv(self._dataset_path, quote_char='"')
        except FileNotFoundError:
            # Initialize an empty DataFrame if the file does not exist
            self._dataset = pl.DataFrame(
                schema={
                    "sample_id": pl.Utf8,
                    "timestamp": pl.Float64,
                    "user_input": pl.Utf8,
                    "retrieved_context": pl.Utf8,
                    "model_rag_evaluation_assessment@v0.0.1": pl.Utf8,
                }
            )

    @property
    def dataset(self) -> pl.DataFrame:
        if self._dataset is None:
            self._setup_dataset()
        return self._dataset  # type: ignore

    @property
    def dataset_path(self) -> str:
        if self._dataset_path is None:
            self._setup_dataset()
        return self._dataset_path  # type: ignore

    def _from_documents_to_string(self, documents: list[Document]) -> str:
        """Convert a list of documents to a single string.

        Args:
            documents: The list of documents to convert.

        Returns:
            The concatenated string of the documents.
        """
        return " ".join([doc.page_content for doc in documents])

    def has_user_input(self, user_input: str) -> bool:
        """Check if the user input is already in the dataset.

        Args:
            user_input: The user input to check.

        Returns:
            True if the user input is in the dataset, False otherwise.
        """
        return user_input in self.dataset["user_input"]

    def add_entry(self, model_response: ModelResponse):
        """Add a new entry to the dataset.

        Args:
            model_response: The model response to add to the dataset.
        """
        entry = pl.DataFrame(
            {
                "sample_id": f"s_{len(self.dataset) + 1}",
                "timestamp": time.time(),
                "user_input": model_response.question,
                "retrieved_context": self._from_documents_to_string(
                    model_response.context
                ),
                "model_rag_evaluation_assessment@v0.0.1": model_response.answer,
            }
        )
        self._dataset = pl.concat([self.dataset, entry], how="vertical")

    def save(self):
        """Save the dataset to the CSV file."""
        self.dataset.write_csv(self.dataset_path, quote_char='"')

    def generate_entries(self, questions: list[str], runnable: RunnableSerializable):
        """Generate entries for the dataset by invoking the RAG chain on a list of questions.

        Args:
            questions: The list of questions to generate entries for.
            rag_chain: The RAG chain to use for generating the entries.
        """
        for question in questions:
            if self.has_user_input(question):
                continue

            response: ModelResponse = runnable.invoke(question)
            self.add_entry(response)
        self.save()


# endregion


# region SessionManager
class SessionManager(metaclass=Singleton):
    def __init__(self):
        self.vectorstore_manager = VectorstoreManager()
        self.model_manager = ModelManager()
        self.dataset_manager = DatasetManager()


# endregion
