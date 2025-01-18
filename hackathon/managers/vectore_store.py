import os

from hackathon.utils.settings.settings_provider import SettingsProvider
from langchain_chroma.vectorstores import Chroma
from langchain_core.vectorstores import VectorStore, VectorStoreRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyMuPDFLoader,
    Docx2txtLoader,
    TextLoader,
    WebBaseLoader,
)
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
            model_name=self.settings_provider.get_embeddings_model_name(),
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs,
        )

        self._vectorstore = Chroma(
            persist_directory=self.settings_provider.get_vectorstore_path(),
            embedding_function=self._embeddings,
        )

        # Check if the knowledge base must be loaded
        # to avoid loading it multiple times
        if len(self.vectorstore.get()["documents"]) == 0:  # type: ignore
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

    def _load_knowledge_base(self, dir_path: str | None = None):
        """Load knowledge base from a directory into the vectorstore.

        Args:
            directory_path: The path to the directory containing the knowledge base.
                If None, the default knowledge base directory is used.

        """

        if self.settings_provider.is_debug():
            self._load_debug_knowledge_base()
            return

        if not dir_path:
            directory_path = self.settings_provider.get_knowledge_base_path()
        else:
            directory_path = dir_path

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
                loader_cls=cls,  # type: ignore
            )
            documents.extend(loader.load())

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=512, chunk_overlap=20
        )
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

    def _load_debug_knowledge_base(self):
        urls = [
            "https://lilianweng.github.io/posts/2023-06-23-agent/",
            "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
            "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
        ]

        docs = [WebBaseLoader(url).load() for url in urls]
        docs_list = [item for sublist in docs for item in sublist]

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=100, chunk_overlap=50
        )
        doc_splits = text_splitter.split_documents(docs_list)
        for doc in tqdm(doc_splits, desc="Adding documents to vectorstore"):
            self.vectorstore.add_texts(
                texts=[doc.page_content],
                metadatas=[doc.metadata],
            )
