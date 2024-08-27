import streamlit as st
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://sakair0903:glW4l6U3XgTXCqoL@cluster-ootsuka.qpezv.mongodb.net/")
db = client["mydb"]  # Replace with your database name

def get_nippo():
    collection = db["nippo"]  # Replace with your collection name
    nippo =  list(collection.find()) 
    return nippo

def get_user():
    collection = db["user"]  # Replace with your collection name
    users =  list(collection.find()) 
    return users





