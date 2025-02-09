from hackathon.enums import LLMProvider
from hackathon.utils.settings.settings_provider import SettingsProvider
from hackathon.utils.singleton import Singleton
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.language_models.chat_models import BaseChatModel
import logging
import warnings

with warnings.catch_warnings(action="ignore"):
    from langchain_ibm import ChatWatsonx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelManager(metaclass=Singleton):
    def __init__(self):
        self._model = None
        self.settings_provider = SettingsProvider()  # type: ignore

    def _setup_model(self):
        match self.settings_provider.get_model_provider():
            case LLMProvider.OPEN_AI:
                self._setup_openai_model()
            case LLMProvider.IBM:
                self._setup_ibm_model()
            case LLMProvider.GOOGLE:
                self._setup_google_model()
            case _:
                raise ValueError("Invalid model provider")

    def _setup_openai_model(self):
        # Configure the model_name with environment variables and settings
        model_name = self.settings_provider.get_openai_model_name()

        # Initialize ChatOpenAI instance
        self._model = ChatOpenAI(model=model_name, temperature=self._get_temperature())

    def _setup_google_model(self):
        # Configure the model_name with environment variables and settings
        self._model = ChatGoogleGenerativeAI(
            model=self.settings_provider.get_google_model_name(),  # type: ignore
            temperature=self._get_temperature(),
        )

    def _setup_ibm_model(self):
        # Configure the model_name with environment variables and settings
        self._model = ChatWatsonx(
            model_id=self.settings_provider.get_ibm_model_name(),  # type: ignore
            url=self.settings_provider.get_ibm_endpoint_url(),  # type: ignore
            project_id=self.settings_provider.get_ibm_project_id(),  # type: ignore
            params={
                "temperature": self._get_temperature(),
            },
        )

    def _get_temperature(self) -> float:
        return self.settings_provider.get_model_temperature()

    @property
    def model(self) -> BaseChatModel:
        if not self._model:
            self._setup_model()
        return self._model  # type: ignore
