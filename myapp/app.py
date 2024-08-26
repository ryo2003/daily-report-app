import streamlit as st
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://root:password@mongodb:27017/")
db = client["mydb"]  # Replace with your database name
collection = db["mycollection"]  # Replace with your collection name

# Fetch data from MongoDB
documents = list(collection.find())

# Display data in Streamlit
st.title("MongoDB Data")

if documents:
    for doc in documents:
        st.write(doc)
else:
    st.write("No data found.")

# Close the connection
client.close()

