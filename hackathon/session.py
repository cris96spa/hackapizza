from dotenv import load_dotenv
from hackathon.managers.dataset_manager import DatasetManager
from hackathon.managers.model_manager import ModelManager
from hackathon.managers.mongodb_store_manager import MongoDBStoreManager
from hackathon.managers.vectore_store import VectorstoreManager
from hackathon.utils.singleton import Singleton
import logging
from langfuse.callback import CallbackHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()


class SessionManager(metaclass=Singleton):
    def __init__(self):
        self.vectorstore_manager = VectorstoreManager()
        self.mongo_db_manager = MongoDBStoreManager()
        self.model_manager = ModelManager()
        self.dataset_manager = DatasetManager()


# endregion
