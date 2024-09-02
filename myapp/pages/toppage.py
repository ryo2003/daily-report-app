import streamlit as st
import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/mount/src/nippo/myapp/utils/')))
from data_fetch import get_username

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/mount/src/nippo/myapp/frontend/')))
from component_list import hide_sidebar, hide_side_button

hide_side_button()




if st.session_state.get("success_id"):
    userid = st.session_state.get("success_id")
    username = get_username(userid)
    st.write("お疲れ様です、"+username+"さん。日報管理システムへようこそ!")


if st.button("マイページ"):
    # クエリパラメータを設定して、search.pyページに遷移
    st.switch_page("pages/mypage.py")

if st.button("日報検索ページ"):
    # クエリパラメータを設定して、search.pyページに遷移
    st.switch_page("pages/search_nippo.py")

if st.button("vector"):
    # クエリパラメータを設定して、search.pyページに遷移
    st.switch_page("pages/vector_search.py")


import streamlit as st
from st_bridge import bridge, html

data = bridge("nippo-bridge", default="No button is clicked")

# Define HTML with JavaScript to handle button clicks
html(f"""
<div style="background-color: whitesmoke; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
    <div style="font-size: 16px; color: dimgray;">Username: ayachan</div>
    <div style="font-size: 16px; color: dimgray;">Purpose: 提案・見積もり</div>
    <div style="font-size: 16px; color: dimgray;">Customer: PQR株式会社</div>
    <div style="font-size: 12px; color: green;">2024-08-29 03:33:31.812000</div>
    <button style="margin-top: 10px; padding: 8px 16px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;" 
            onClick="stBridges.send('nippo-bridge', 'Nippo ID: 66cfdb1c49886065db244707')">View Details</button>
</div>
""")

# Display the data returned by the bridge (based on which button was clicked)
st.write(data)

# Optionally, you can perform more logic depending on the returned data
if "Nippo ID" in data:
    st.success(f"Details fetched for {data}")

###########


import openai
import streamlit as st
from pymongo import MongoClient
import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/mount/src/nippo/myapp/utils/')))

load_dotenv()
api_key = st.secrets["API_KEY"]
MONGO_URI = st.secrets["MONGO_URI"]
api_base = st.secrets["API_BASE"]

mongo_client = MongoClient(MONGO_URI)
db = mongo_client["mydb"]
collection = db["nippo_contents"]

import os
from openai import AzureOpenAI

client = AzureOpenAI(
  api_key =api_key,  
  api_version = "2023-05-15",
  azure_endpoint =api_base
)

# Azure OpenAIクライアントの初期化
# エンベディングを取得するためのテストテキスト
test_text = "This is a sample text for testing embeddings."

# 結果を表示
#st.write(response.model_dump_json(indent=2))


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
    collection.insert_one(newdata)

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
                            'index': 'vector_index',  # Replace with your actual index name
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


def main():
    st.title("Query Embedding and Similar Document Search")

    query = st.text_input("Enter your query:")
    
    if st.button("Find Similar Documents"):
        st.write("oush")
        try:
            # Create the embedding for the query
            embedding = create_embedding(query)
            #st.write("Generated Embedding:", embedding)
            
            # Find similar documents in the MongoDB collection
            similar_documents = find_similar_documents(embedding)
            #st.write("Similar Documents:", similar_documents)
            
            # Get the document with the highest score
            highest_score_doc = get_highest_score_document(similar_documents)
            
            if highest_score_doc:
                st.success("Document with the highest score:")
                st.write(f"Text: {highest_score_doc['text']}")
                st.write(f"Score: {highest_score_doc['score']}")
            else:
                st.warning("No similar documents found.")
        
        except Exception as err:
            st.error(f"Error: {err}")

main()

