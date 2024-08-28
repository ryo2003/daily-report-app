import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()
mongo_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_URI)
db = client["mydb"]  # Replace with your database name

# submit nippo byhands
def submit_byhands(submit_user_id,submit_data):
    # submit_data is dictionary containing data user input on createbyhands page
    collection = db["nippo"]
    newdata = {
        "user_id":submit_user_id,
        "contents":submit_data["内容"],
        "good": [None,None],
        "bookmark":[None],
        "purpose":submit_data["訪問目的"],
        "customer":submit_data["企業名"]
    }
    collection.insert_one(newdata)