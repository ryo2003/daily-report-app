import os
import sys

from openai import AzureOpenAI
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import pytz
import json

load_dotenv()

def extract_keys_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    keys_list = list(data.keys())
    return keys_list

def create_question(chatlog: list[dict]) -> str:
    # return 'こんにちは! create_question が呼ばれたよ！' + str(len(chatlog))
    deployment_name = "gpt-4o-mini"  # デプロイ名
    model_name = "gpt-4o-mini"  # モデル名
    api_key = os.getenv('API_KEY')
    api_base = os.getenv('API_BASE')

    client = AzureOpenAI(
    api_key =api_key,  
    api_version = "2023-05-15",
    azure_endpoint =api_base
    )

    prompt = '以下の会話をもとに、ステップバイステップで日報作成に必要な情報を聞き出すような質問をしてください。'
    mess = [{"role": "system", "content": prompt}] + [{"role": chat["name"], "content": chat["msg"]} for chat in chatlog]
    print("mess",mess)
    try:
        response = client.chat.completions.create(
            model=model_name , # model = "deployment_name".
            messages = mess,
        )
    except Exception as e:
        return 'エラーが発生しました。'
    
    return response.choices[0].message.content

def create_nippo(chatlog: list[dict]) -> str:
    # return 'こんにちは! create_nippo が呼ばれたよ！' + str(len(chatlog))
    deployment_name = "gpt-4o-mini"  # デプロイ名
    model_name = "gpt-4o-mini"  # モデル名
    api_key = os.getenv('API_KEY')
    api_base = os.getenv('API_BASE')

    client = AzureOpenAI(
    api_key =api_key,  
    api_version = "2023-05-15",
    azure_endpoint =api_base
    )

    prompt = '以下の会話をもとに、hallucinationに気をつけて日報を作成してください。'
    mess = [{"role": "system", "content": prompt}] + [{"role": chat["name"], "content": chat["msg"]} for chat in chatlog]
    print("mess",mess)
    try:
        response = client.chat.completions.create(
            model=model_name ,
            messages = mess,
        )
    except Exception as e:
        return 'エラーが発生しました。'

    return response.choices[0].message.content

def get_chatlog(chatlogId) -> list:
    print("call get_chatlog!!!!")
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['mydb']
    collection = db['chat_log']

    chatlog = collection.find_one({"_id": chatlogId})

    print("chatlog",chatlog)

    if chatlog is None:
        print("chatlog is None")
        return []
    
    return chatlog.get("log_data", [])

def get_category(chatlogId) -> str:
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['mydb']
    collection = db['chat_log']

    chatlog = collection.find_one({"_id": chatlogId})

    if chatlog is None:
        return ""
    
    return chatlog.get("category", "")

def add_catdata(chatlogId, category):
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['mydb']
    collection = db['chat_log']

    collection.update_one({"_id": chatlogId}, {"$set": {"category": category}}, upsert=True)

def add_chatlog(chatlogId, chatlog):
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['mydb']
    collection = db['chat_log']

    collection.update_one(
        {"_id": chatlogId},
        {"$push": {"log_data": chatlog}},
        upsert=True  # ドキュメントが存在しない場合は新規作成
    )
    return

def pop_chatlog(chatlogId):
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['mydb']
    collection = db['chat_log']

    collection.update_one(
        {"_id": chatlogId},
        {"$pop": {"log_data": 1}}
    )
    return

def reset_log(chatlogId):
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['mydb']
    collection = db['chat_log']

    collection.update_one({"_id": chatlogId}, {"$set": {"log_data": []}})
    collection.update_one({"_id": chatlogId}, {"$set": {"category": ""}})
    return

def make_nippo_data(nippo : str, eventId : ObjectId, purpose : str, chatlogId : ObjectId = None):
    print("make_nippo_data")
    print("nippo: ",nippo)

    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['mydb']

    # 削除パート
    collection = db['event']
    nippo_id = collection.find_one({"_id": eventId})["nippo_id"]
    if nippo_id is not None:
        collection = db['nippo']
        if collection.find_one({"_id": nippo_id}) is not None:
            collection.delete_one({"_id": nippo_id})
        collection = db['user']
        collection.update_one(
            {"nippo_id": nippo_id},
            {"$pull": {"nippo_id": nippo_id}}
        )
    # 削除パート終了
    
    collection = db['event']

    userId = collection.find_one({"_id": eventId})["user_id"]
    customer = collection.find_one({"_id": eventId})["customer"]

    print("userId",userId)
    print("customer",customer)

    event_time = collection.find_one({"_id": eventId})["start_time"]
    collection = db['nippo']
    nippo_data = {
        "user_id": userId,
        "event_id": eventId,
        "contents": nippo,
        "good" : [],
        "bookmark" : [],
        "purpose": purpose,
        "customer": customer,
        "chat_log_id": chatlogId,
        "timestamp": datetime.now() + pytz.timezone('Asia/Tokyo').utcoffset(datetime.now()),
        "event_time": event_time
    }

    res = collection.insert_one(nippo_data)

    nippo_id = res.inserted_id
    collection = db['user']
    collection.update_one(
        {"_id": userId},
        {"$push": {"nippo_id": nippo_id}}
    )

    collection = db['event']
    collection.update_one(
        {"_id": eventId},
        {"$set": {"nippo_id": nippo_id}}
    )

    collection = db['chat_log']
    collection.update_one(
        {"_id": chatlogId},
        {"$set": {"nippo_id": nippo_id}}
    )
    
    return
