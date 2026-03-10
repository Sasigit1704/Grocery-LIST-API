from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["groceryDB"]

grocery_collection = db["grocery_lists"]
metadata_collection = db["lists_metadata"]