from pydantic_settings import BaseSettings, SettingsConfigDict

from hackathon.enums import LLMProvider


class Settings(BaseSettings):
    """
    All the settings for the application.
    """

    # Debug mode
    debug: bool

    # Data path
    data_path: str
    competition_data: str
    menu_path: str

    # Vectorstore paths
    vectorstore_relative_path: str
    debug_vectorstore_relative_path: str

    # Knowledge base path
    knowledge_base_path: str

    # Dataset path
    dataset_path: str

    # Embeddings model name
    embeddings_model_name: str

    model_provider: LLMProvider

    # Model settings
    model_temperature: float = 0.0

    openai_model_name: str | None = None

    ibm_model_name: str | None = None

    ibm_project_id: str | None = None
    ibm_endpoint_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=".rag.settings",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )
