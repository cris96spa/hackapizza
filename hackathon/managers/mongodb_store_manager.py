import pymongo
from pymongo import MongoClient
from tqdm import tqdm
import torch
import logging
from hackathon.models import MenuMetadata, DishMetadata

from hackathon.utils.settings.settings_provider import SettingsProvider

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDBStoreManager:
    def __init__(self):
        self.settings_provider = SettingsProvider()
        self.client = MongoClient(self.settings_provider.get_mongo_db_uri())
        self.db = self.client["hackathon"]
        self.collection = self.db["documents"]

    def describe_collection(self) -> str:
        """
        The method returns a string containing every field in the collection, each with every possible values.
        """

        documents = self.collection.find()

        menu_metadata_keys = MenuMetadata.model_fields.keys()
        dish_metadata_keys = DishMetadata.model_fields.keys()
        # Merge the keys
        base_model_keys = set(menu_metadata_keys).union(dish_metadata_keys)


        keys = set()
        for document in documents:
            document_keys = document.keys()

            keys.update(document_keys)
        
        keys = keys.intersection(base_model_keys)

        description = ""
        for key in keys:
            values = self.collection.distinct(key)

            description += f"{key}: {values}\n"

        # Include json schema of menu_metadata and dish_metadata
        description += str(MenuMetadata.model_json_schema()) + "\n"
        description += str(DishMetadata.model_json_schema()) + "\n"

        return description
    