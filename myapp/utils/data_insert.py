import sys
import os

from dotenv import load_dotenv
from bson import ObjectId
from pymongo import MongoClient

load_dotenv()
mongo_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_URI)
db = client["mydb"] 

def insert_chat(event_id,user_id):
    try:
        collection = db["chat_log"]
        data={
            "user_id":user_id
        }
        res = collection.collection.insert_one(data)
        print(type(res._id))
        update_data = {
        "$set": {
            "chatlog_id":  ObjectId(res._id)
            }
        }
        result = collection.update_one({"_id": ObjectId(event_id)}, update_data)
        return res["_id"]
    except:
        return 0




