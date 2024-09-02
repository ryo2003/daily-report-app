import os,sys
import streamlit as st
from pymongo import MongoClient
import asyncio
from beanie import Document, init_beanie, PydanticObjectId
from motor.motor_asyncio import AsyncIOMotorClient

from dotenv import load_dotenv
import pymongo
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))
from models import Nippo

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")



# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["mydb"]  # Replace with your database name

def get_nippo():
    collection = db["nippo"]  # Replace with your collection name
    nippo =  collection.find() 
    return nippo

def get_user():
    collection = db["user"]  # Replace with your collection name
    users =  collection.find()
    return users

def get_username(user_id):
    # Access the users collection
    users_collection = db["user"]  # Replace with your users collection name
    
    # Find the user document that matches the given user_id
    user = users_collection.find_one({"_id": user_id})
    
    # Return the username if found, otherwise return None
    return user["user_name"] if user else None


    
def get_id_from_username(username):
    users_collection = db["user"]
    user = users_collection.find_one({"user_name": username})
    return user["_id"]

# Initialize MongoDB client
def get_client(event_loop=None):
    if event_loop:
        client = AsyncIOMotorClient(
            MONGO_URI,
            io_loop=event_loop,
        )
    else:
        client = AsyncIOMotorClient(
            MONGO_URI,
        )
    return client

# Initialize the database with the given collections
async def init_database(client, models=[Nippo]):
    database = client.get_database(name='mydb')
    await init_beanie(database=database, document_models=models)

# e.g. filter = {"user_id": user_id}
async def fetch_async(filter=None,model=Nippo):
    if filter:
        data = await model.find(filter,fetch_links=True).to_list()
    else:
        data = await model.find(fetch_links=True).to_list()
    return data

