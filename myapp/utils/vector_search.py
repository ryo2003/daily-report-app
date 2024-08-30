import os
from openai import AzureOpenAI
import streamlit as st
import json
from pymongo import MongoClient
import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))

load_dotenv()
api_key = os.getenv("API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
api_base = os.getenv("API_BASE")

mongo_client = MongoClient(MONGO_URI)
db = mongo_client["mydb"]
collection = db["nippo"]

client = AzureOpenAI(
  api_key =api_key,  
  api_version = "2023-05-15",
  azure_endpoint =api_base
)

def create_embedding(contents="this is sample text", purpose='',model="text-embedding-3-large"):
    # Create an embedding using the OpenAI API
    text = contents + purpose
    response = client.embeddings.create(
        model=model,  # 指定されたエンベディングモデル名
        input=text
    )   
    # Extract the embedding from the response
    embedding = json.loads(response.model_dump_json(indent=2))['data'][0]['embedding']

    newdata = {
        "embedding":embedding,
        "text": text
    }
    #collection.insert_one(newdata)

    #st.write('embedding', embedding)

    return embedding

# Function to find the document with the highest score
def get_highest_score_document(similar_documents):
    if not similar_documents:
        return None
    
    highest_score_doc = max(similar_documents, key=lambda doc: doc['score'])
    return highest_score_doc


# Function to find similar documents using MongoDB Atlas Search
def find_similar_documents(embedding, k=5):
    try:
        # MongoDB aggregate query to find similar documents
        pipeline = [
                    {
                        '$vectorSearch': {
                            'index': 'vector_nippo',  # Replace with your actual index name
                            'path': 'embedding',  # Path to the embedding field in your documents
                            'queryVector': embedding,  # The input vector you're comparing against
                            'numCandidates': 100,  # Adjust the number of candidates as needed
                            'limit': k  # Number of results you want to return
                        }
                    },
                    {
                        '$addFields': {
                            'score': { '$meta': 'vectorSearchScore' }  # Ensure this metadata is added correctly
                        }
                    }
                    ]
        documents = list(collection.aggregate(pipeline))
        return documents
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []

