import os
from bson import ObjectId
import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
mongo_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_URI)
db = client["mydb"]  # Replace with your database name

# submit nippo byhands
def submit_byhands(submit_data):
    # submit_data is dictionary containing data user input on createbyhands page
    collection = db["nippo"]
    newdata = {
        "contents":submit_data["内容"],
        "good": [None,None],
        "bookmark":[None],
        "purpose":submit_data["訪問目的"],
        "customer":submit_data["企業名"]
    }
    collection.insert_one(newdata)
    
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

