import os
from hackathon.enums import LLMProvider
from hackathon.utils.settings.settings import Settings
from hackathon.utils.singleton import Singleton
from langfuse.callback import CallbackHandler


class SettingsProvider(metaclass=Singleton):
    """
    This class is a singleton that provides access to the settings for the RAG model.
    """

    def __init__(self):
        self.settings = Settings()  # type: ignore
        self._langfuse_config = None

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

    def get_menu_path(self) -> str:
        return os.path.join(self.settings.competition_data, self.settings.menu_path)

    def get_techniques_json_path(self) -> str:
        return os.path.join(
            self.settings.competition_data,
            self.settings.entities_path,
            self.settings.techniques_json,
        )

    def get_cooking_manual_path(self) -> str:
        return os.path.join(
            self.settings.competition_data,
            self.settings.misc_path,
            self.settings.manuale_cucina_path,
        )

    def get_galactic_code_path(self) -> str:
        return os.path.join(
            self.settings.competition_data,
            self.settings.codice_galattico_dir_path,
            self.settings.codice_galattico_path,
        )

    def get_dish_mapping_path(self) -> str:
        return os.path.join(
            self.settings.competition_data,
            self.settings.misc_path,
            self.settings.dish_mapping,
        )

    def get_distance_csv_path(self) -> str:
        return os.path.join(
            self.settings.competition_data,
            self.settings.misc_path,
            self.settings.distanze_path,
        )

    def get_dataset_path(self) -> str:
        return os.path.join(self.settings.data_path, self.settings.dataset_path)

    def get_embeddings_model_name(self) -> str:
        return self.settings.embeddings_model_name

    def get_model_provider(self) -> LLMProvider:
        return self.settings.model_provider

    def get_embeddings_provider(self) -> LLMProvider:
        return self.settings.embedding_provider

    def get_openai_model_name(self) -> str | None:
        return self.settings.openai_model_name

    def get_google_model_name(self) -> str | None:
        return self.settings.google_model_name

    def get_ibm_model_name(self) -> str | None:
        return self.settings.ibm_model_name

    def get_model_temperature(self) -> float:
        return self.settings.model_temperature

    def get_ibm_project_id(self) -> str | None:
        return self.settings.ibm_project_id

    def get_ibm_endpoint_url(self) -> str | None:
        return self.settings.ibm_endpoint_url

    def get_mongo_db_uri(self) -> str:
        return self.settings.mongo_db_uri

    def get_dishes_json_path(self) -> str:
        return os.path.join(
            self.settings.competition_data,
            self.settings.entities_path,
            self.settings.dishes_json,
        )

    def get_chefs_json_path(self) -> str:
        return os.path.join(
            self.settings.competition_data,
            self.settings.entities_path,
            self.settings.chefs_json,
        )

    def get_licenses_json_path(self) -> str:
        return os.path.join(
            self.settings.competition_data,
            self.settings.entities_path,
            self.settings.licenses_json,
        )

    def get_langfuse_config(self) -> CallbackHandler:
        if self._langfuse_config is None:
            langfuse_handler = CallbackHandler()
            self._langfuse_config = {"callbacks": [langfuse_handler]}
        return self._langfuse_config

    def get_neo4j_url(self) -> str:
        return self.settings.neo4j_url

    def get_neo4j_username(self) -> str:
        return self.settings.neo4j_username

    def get_neo4j_password(self) -> str:
        return self.settings.neo4j_password
