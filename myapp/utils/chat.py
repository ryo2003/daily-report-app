import os
import sys

from openai import AzureOpenAI
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId

load_dotenv()


default_question = ['お疲れ様です。今回の営業の目的を教えてください。']

def create_question(chatlog: list[dict]) -> str:
    return 'こんにちは! create_question が呼ばれたよ！' + str(len(chatlog))
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
    try:
        response = client.chat.completions.create(
            model=model_name , # model = "deployment_name".
            messages = [{"role": "system", "content": prompt}] + [{"role": chat["name"], "content": chat["msg"]} for chat in chatlog],
        )
    except Exception as e:
        return 'エラーが発生しました。'
    
    return response.choices[0].message.content

def create_nippo(chatlog: list[dict]) -> str:
    return 'こんにちは! create_nippo が呼ばれたよ！' + str(len(chatlog))
    deployment_name = "gpt-4o-mini"  # デプロイ名
    model_name = "gpt-4o-mini"  # モデル名
    api_key = os.getenv('API_KEY')
    api_base = os.getenv('API_BASE')

    client = AzureOpenAI(
    api_key =api_key,  
    api_version = "2023-05-15",
    azure_endpoint =api_base
    )

    prompt = '以下の会話をもとに、hallucinationに気をつけて日報を作成してください。\n\n'
    try:
        response = client.chat.completions.create(
            model=model_name ,
            messages = [{"role": "system", "content": prompt}] + [{"role": chat["name"], "content": chat["msg"]} for chat in chatlog],
        )
    except Exception as e:
        return 'エラーが発生しました。'

    

    return response.choices[0].message.content

def get_chatlog(chatlogId) -> list:
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['mydb']
    collection = db['chat_log']

    print("call get_chatlog!!!!")
    print("chatlogId",chatlogId)
    print('dtype',type(chatlogId))


    chatlog = collection.find_one({"_id": chatlogId})

    print("chatlog",chatlog)

    if chatlog is None:
        print("chatlog is None")
        return []
    
    return chatlog.get("log_data", [])

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

def make_nippo_data(nippo : str, chatlogId, eventId):
    print("make_nippo_data")
    print("nippo: ",nippo)

    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['mydb']

    collection = db['event']
    userId = collection.find_one({"_id": eventId})["user_id"]
    customer = collection.find_one({"_id": eventId})["customer"]

    print("userId",userId)
    print("customer",customer)

    collection = db['nippo']
    res = collection.insert_one({
        "user_id": userId,
        "chatlog_id": chatlogId,
        "event_id": eventId,
        "contents": nippo,
        "good" : [],
        "bookmark" : [],
        "purpose": "",
        "customer": customer,
    })

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
