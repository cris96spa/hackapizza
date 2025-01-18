import os
from hackathon.utils.settings.settings import Settings
from hackathon.utils.singleton import Singleton


class SettingsProvider(metaclass=Singleton):
    """
    This class is a singleton that provides access to the settings for the RAG model.
    """

    def __init__(self):
        self.settings = Settings()  # type: ignore

    def is_debug(self) -> bool:
        return self.settings.debug

    def get_vectorstore_path(self) -> str:
        if self.is_debug():
            return self._get_debug_vectorstore_path()
        else:
            return self._get_vectorstore_path()

    def _get_vectorstore_path(self) -> str:
        return os.path.join(
            self.settings.data_path, self.settings.vectorestore_relative_path
        )

    def _get_debug_vectorstore_path(self) -> str:
        return os.path.join(
            self.settings.data_path, self.settings.debug_vectorstore_relative_path
        )

    def get_knowledge_base_path(self) -> str:
        return os.path.join(self.settings.data_path, self.settings.knowledge_base_path)

    def get_dataset_path(self) -> str:
        return os.path.join(self.settings.data_path, self.settings.dataset_path)

    def get_embeddings_model_name(self) -> str:
        return self.settings.embeddings_model_name

    def get_model_name(self) -> str:
        return self.settings.model_name

    def get_model_temperature(self) -> float:
        return self.settings.model_temperature
