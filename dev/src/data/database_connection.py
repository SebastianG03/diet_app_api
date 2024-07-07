import json
import motor.motor_asyncio
from pymongo.errors import ServerSelectionTimeoutError
from tenacity import (
    wait_exponential, 
    retry, 
    stop_after_attempt
    )
from models import Customer, CustomerInfo
from .errors import (
    RepositoryNotConnected,
)

class DatabaseConnection:
    
    def __init__(self):
        self.client = self.connect_mongodb(self)
        self.database = self.client.get_database(self.get_mongodb_data(key="db"))


    def get_mongodb_data(self, key):
        with open("db_information.json", encoding="utf-8") as f:
            db_info = json.load(f)
            return db_info[key]

    def connect_mongodb(self):
        mongodb_url = self.get_mongodb_data(key="connection")
        return motor.motor_asyncio.AsyncIOMotorClient(mongodb_url)
        
    @retry(
        wait = wait_exponential(multiplier = 0.1), stop = stop_after_attempt(3), reraise = True
    )
    def connect_collection(self, collection: str):
        try:
            if collection not in self.database.list_collection_names():
                collection = self.database.create_collection(collection)
            return self.database.get_collection(collection)
        except ServerSelectionTimeoutError as err:
            raise RepositoryNotConnected from err