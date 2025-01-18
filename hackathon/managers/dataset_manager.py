from hackathon.utils.settings.settings_provider import SettingsProvider
from hackathon.utils.singleton import Singleton
from langchain_core.documents import Document
from hackathon.graph.models import CSVEntry
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
                    "row_id": pl.Int64,
                    "result": pl.Utf8,
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

    def add_entry(self, entry: CSVEntry) -> None:
        """Add a new entry to the dataset.

        Args:
            model_response: The model response to add to the dataset.
        """
        entry = pl.DataFrame(
            {
                "row_id": entry.question_id,
                "result": entry.result,
            }
        )
        self._dataset = pl.concat([self.dataset, entry], how="vertical")

    def save(self):
        """Save the dataset to the CSV file."""
        self.dataset.write_csv(self.dataset_path, quote_char='"', include_header=True)
