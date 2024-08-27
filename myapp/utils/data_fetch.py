import streamlit as st
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://sakair0903:glW4l6U3XgTXCqoL@cluster-ootsuka.qpezv.mongodb.net/")
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



