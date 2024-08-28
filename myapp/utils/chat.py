import os
import sys

from openai import AzureOpenAI
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId

load_dotenv()


default_question = ['お疲れ様です。今回の営業の目的を教えてください。']

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
    try:
        response = client.chat.completions.create(
            model=model_name , # model = "deployment_name".
            messages = [{"role": "system", "content": prompt}] + [{"role": chat["name"], "content": chat["msg"]} for chat in chatlog],
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

    chatlog = collection.find_one({"_id": ObjectId(chatlogId)})

    if chatlog is None:
        return []
    
    return chatlog.get("event", [])