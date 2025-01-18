from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    All the settings for the application.
    """

    # Debug mode
    debug: bool

    # Data path
    data_path: str

    # Vectorstore paths
    vectorstore_relative_path: str
    debug_vectorstore_relative_path: str

    # Knowledge base path
    knowledge_base_path: str

    # Dataset path
    dataset_path: str

    # Embeddings model name
    embeddings_model_name: str

    # Model settings
    model_name: str
    model_temperature: float

    model_config = SettingsConfigDict(
        env_file=".rag.settings", env_file_encoding="utf-8", case_sensitive=False
    )
