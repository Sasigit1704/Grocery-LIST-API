from pymongo import MongoClient
from utilities.constants import (
    MONGO_URL,
    DATABASE_NAME,
    GROCERY_COLLECTION,
    METADATA_COLLECTION
)

class MongoDB:
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client[DATABASE_NAME]

        self.grocery_collection = self.db[GROCERY_COLLECTION]
        self.metadata_collection = self.db[METADATA_COLLECTION]


mongo_db = MongoDB()


def get_db():
    return mongo_db