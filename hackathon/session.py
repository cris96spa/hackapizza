from dotenv import load_dotenv
from hackathon.managers.dataset_manager import DatasetManager
from hackathon.managers.model_manager import ModelManager
from hackathon.managers.neo4j_store_manager import Neo4jStoreManager
from hackathon.utils.singleton import Singleton
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()


class SessionManager(metaclass=Singleton):
    def __init__(self):
        self.neo4j_manager = Neo4jStoreManager()
        self.model_manager = ModelManager()
        self.dataset_manager = DatasetManager()


# endregion
