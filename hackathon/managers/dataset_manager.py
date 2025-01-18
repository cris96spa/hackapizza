from hackathon.utils.settings.settings_provider import SettingsProvider
from hackathon.utils.singleton import Singleton
from langchain_core.documents import Document
from hackathon.graph.models import ModelResponse
from langchain_core.runnables import RunnableSerializable
import polars as pl
import time


class DatasetManager(metaclass=Singleton):
    """Singleton class for managing the dataset containing the interactions with the
    RAG system.
    """

    def __init__(self):
        self._dataset = None
        self._dataset_path = None
        self.settings_provider = SettingsProvider()  # type: ignore

    def _setup_dataset(self):
        """Setup the dataset by loading the CSV file containing the interactions with the
        RAG system.
        """

        self._dataset_path = self.settings_provider.get_dataset_path()
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

    def add_entry(self, model_response: ModelResponse) -> None:
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
