import json
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError
from tenacity import (
    wait_exponential, 
    retry, 
    stop_after_attempt
    )
from data.errors import (
    RepositoryNotConnected,
)

class DatabaseConnection:
     
    
    def __init__(self):
        self.connection_url = "mongodb+srv://db_developer:dev-mongo12@daseudla.ttyxr35.mongodb.net/?retryWrites=true&w=majority&appName=DaseUdla"
        self.db_name = "dietApp"
        self.collections = ["recipes", "ingredients"]
        self.client = self.connect_mongodb()
        self.database = self.client.get_database(self.db_name)


    def connect_mongodb(self) -> AsyncIOMotorClient:
        return motor.motor_asyncio.AsyncIOMotorClient(self.connection_url)
        
    @retry(
        wait = wait_exponential(multiplier = 0.1), stop = stop_after_attempt(3), reraise = True
    )
    async def connect_collection(self, collection: str) -> AsyncIOMotorCollection:
        try:
            if collection not in self.database.list_collection_names():
                collection = self.database.create_collection(collection)
            return await self.database.get_collection(collection)
        except ServerSelectionTimeoutError as err:
            raise RepositoryNotConnected from err