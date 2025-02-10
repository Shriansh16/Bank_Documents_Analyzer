import json
from pymongo import MongoClient
import os
import re
from pdf_extractor import PDFExtractor  
from dotenv import load_dotenv

load_dotenv()

class BankInfoStorage:
    def __init__(self, db_name="Bank", collection_name="informations"):
        uri = "mongodb+srv://shrianshsingh16:oNDEadaTWu9UdG5w@sheenu.o2u5s.mongodb.net/?retryWrites=true&w=majority&appName=sheenu"
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def store_info(self,pdf_path):
        obj = PDFExtractor(gemini_api_key=os.getenv("GEMINI_API_KEY"))
        extracted_text = obj.extract_text(pdf_path)

       # print("Extracted Data Type:", type(extracted_text))  # Debugging
        #print("Extracted Data:", extracted_text)  # Debugging

        # Step 1: Extract the JSON string from the dictionary
        if isinstance(extracted_text, dict):
            json_str = next(iter(extracted_text.values()))  # Get the first value (JSON string)
        else:
            print("Error: Extracted text is not a dictionary")
            return

        # Step 2: Remove Markdown-style formatting (` ```json ` and ` ``` `)
        json_str = re.sub(r"```json\n|\n```", "", json_str).strip()

        # Step 3: Convert JSON string to a Python dictionary
        try:
            extracted_data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            return

        # Step 4: Insert the cleaned data into MongoDB
        self.collection.insert_one(extracted_data)  # Now it's a valid MongoDB document

        print("Data successfully stored in MongoDB.")

if __name__ == "__main__":
    storage = BankInfoStorage()
    storage.store_info(pdf_path='Bank Statement Example Final.pdf')
