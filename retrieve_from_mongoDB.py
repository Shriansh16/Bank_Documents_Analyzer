import json
from pymongo import MongoClient
import os

class BankInfoRetrieval:
    def __init__(self, db_name="Bank", collection_name="informations"):
        uri = "mongodb+srv://shrianshsingh16:oNDEadaTWu9UdG5w@sheenu.o2u5s.mongodb.net/?retryWrites=true&w=majority&appName=sheenu"
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def retrieve_latest_info(self):
        # Fetch the latest added document
        latest_doc = self.collection.find_one(sort=[("_id", -1)])

        if latest_doc:
            # Convert MongoDB's ObjectId to string to make it JSON serializable
            latest_doc["_id"] = str(latest_doc["_id"])
            return latest_doc  # Return as JSON-compatible dictionary
        else:
            return None  # No documents found

"""if __name__ == "__main__":
    retriever = BankInfoRetrieval()
    latest_data = retriever.retrieve_latest_info()


    if latest_data:
        print(json.dumps(latest_data, indent=4))  # Print in original JSON format
    else:
        print("No data found.")"""
