from hackathon.utils.settings.settings_provider import SettingsProvider
from hackathon.utils.singleton import Singleton
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelManager(metaclass=Singleton):
    def __init__(self):
        self._model = None
        self.settings_provider = SettingsProvider()  # type: ignore

    def _setup_model(self):
        # Configure the model_name with environment variables and settings
        model_name = self.settings_provider.get_model_name()
        temperature = float(self.settings_provider.get_model_temperature())

        # Initialize ChatOpenAI instance
        self._model = ChatOpenAI(model=model_name, temperature=temperature)

    @property
    def model(self) -> BaseChatModel:
        if not self._model:
            self._setup_model()
        return self._model  # type: ignore
