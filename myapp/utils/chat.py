import os
import sys

from openai import AzureOpenAI
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import pytz
import json

from utils.vector_search import create_embedding

load_dotenv()

def save_new_chatlog(user_id: ObjectId, log_data : list[dict], category : str, nippo_id : ObjectId = ObjectId()):
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['mydb']
    collection = db['chat_log']

    chatlog_data = {
        "user_id": user_id,
        "log_data": log_data,
        "nippo_id": nippo_id,
        "category": category,
    }

    res = collection.insert_one(chatlog_data)
    return res.inserted_id

def get_data(eventId):
    res = {"event": {}, 'chatlog_id' : ObjectId(), "chatlog": [], "category": ""}
    if not eventId:
        print("event idがないよー")
        return res

    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['mydb']
    collection = db['event']

    event = collection.find_one({"_id": eventId})
    if event is None:
        print(f"idが{eventId}のイベントはないよー")
        return res
    
    print("event",event, type(event))
    res["event"] = event
    
    chatlogId = event.get("chatlog_id", ObjectId())
    chatlogId = ObjectId(chatlogId)
    res["chatlog_id"] = chatlogId
    if chatlogId:
        collection = db['chat_log']
        chatlog = collection.find_one({"_id": chatlogId})
        print('-'*100)
        print("chatlog ID",chatlogId)
        print(type(chatlogId))
        print("chatlog",chatlog)
        if event.get("purpose", "") and not chatlog.get("category", ""):
            collection.update_one(
                {"_id": chatlogId},
                {"$set": {"category": event.get("purpose", "")}}
            )
        if chatlog:
            res["chatlog"] = chatlog.get("log_data", [])
            res['category'] = chatlog.get("category", "")
            return res
    
    res["chatlog"] = []
    res['category'] = event.get("purpose", "")
    chatlogId = save_new_chatlog(event["user_id"], [], event.get("purpose", ""))
    res["chatlog_id"] = chatlogId
    collection = db['event']
    collection.update_one(
        {"_id": eventId},
        {"$set": {"chatlog_id": chatlogId}}
    )

    return res

def extract_keys_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    keys_list = list(data.keys())
    return keys_list

def create_question(chatlog: list[dict], other_info : dict) -> str:
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

    print("other_info",other_info)
    prompt = f"""
    あなたは完璧な日報作成システムです。日報作成にあたって必要な情報をユーザーから聞き出したください。
    ただし、1回の発話では1つのことについて質問し、具体的で答えやすい質問を心がけてください。
    また、日報のカテゴリー、相手の企業名、日時、場所については、すでに提供されている情報ですので、それ以外の情報を聞き出してください。
    特に、以下の情報については、優先的にユーザーに聞き出してください。
    - 先方の担当者名
    - 同行者の有無
    - 次回訪問の予定があれば、その日程
    ただし、この内容以外にも必要な情報をなるべく多く聞き出してください。

    日報のカテゴリーは{other_info.get('purpose', '不明')}で、相手の企業名は{other_info.get('customer', '不明')}、日時は{other_info.get('start_time', '不明')}、場所は{other_info.get('address', '不明')}です。
    userが関係ない話をしたときは、「その話題には返答できません。」と返答して、直前のsystemの質問を繰り返してください。
    """
    mess = [{"role": "system", "content": prompt}] + [{"role": chat["name"], "content": chat["msg"]} for chat in chatlog]
    print("mess",mess)

    try:
        response = client.chat.completions.create(
            model=model_name , # model = "deployment_name".
            messages = mess,
        )
    except Exception as e:
        return 'その質問には回答できません。'
    
    return response.choices[0].message.content

def create_nippo(chatlog: list[dict], other_info) -> str:
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

    conversation_text = "\n".join([f"{chat['name']}: {chat['msg']}" for chat in chatlog])

    prompt = f"""
    以下の対話履歴に基づいて、日報の本文を作成してください
    日報のカテゴリーは{other_info.get('purpose', '不明')}で、相手の企業名は{other_info.get('customer', '不明')}、日時は{other_info.get('start_time', '不明')}、場所は{other_info.get('address', '不明')}です。：

    注意1: 日報本文には、「お疲れ様です。」などの本文以外の情報は含めないでください。
    注意2: Hallucinationに気を付けて日報は生成してください。会話履歴に含まれていない情報は合理的に導ける内容以外は含めないでください。
    注意3: 日報のカテゴリー、相手の企業名、日時、場所は、日報本文には含めないで良いです。
    注意4: 日報本文は主語や目的語を適切に設定して、読みやすい文章にしてください。
    注意5: 日報本文は、「今回の営業では」のような形で始めてください。

    対話履歴：
    {conversation_text}

    日報本文：
    """
    mess = [{"role": "system", "content": prompt}]
    print("mess",mess)

    try:
        response = client.chat.completions.create(
            model=model_name ,
            messages = mess,
            max_tokens = 300,
            temperature = 0.5,
            stop=["質問", "続ける", "教えて"]  # 必要に応じてストップワードを設定
        )
        print("daily_report",response)
        daily_report = response.choices[0].message.content
    except Exception as e:
        return 'エラーが発生しました。'

    print("response",response)
    return daily_report

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

def get_chatlog(eventId) -> ObjectId:
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['mydb']
    collection = db['event']

    event = collection.find_one({"_id": eventId})
    if event is None:
        return None
    
    chatlogId = event.get("chatlog_id", None)
    if chatlogId is None:
        return None


def get_event_info(eventId) -> dict:
    if not eventId:
        return {}
    
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['mydb']
    collection = db['event']

    event = collection.find_one({"_id": eventId})

    if event is None:
        return {}
    
    return event

def add_catdata(chatlogId, category):
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['mydb']
    collection = db['chat_log']

    collection.update_one({"_id": chatlogId}, {"$set": {"category": category}}, upsert=True)

def add_chatlog(chatlogId, chatlog):
    if not chatlogId:
        return
    
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

def reset_log(chatlogId : ObjectId, category : str):
    print("reset_log chatlogId: ",chatlogId)
    print("reset_log category: ",category)
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['mydb']
    collection = db['chat_log']

    collection.update_one({"_id": chatlogId}, {"$set": {"log_data": [], "category": category}})
    return

def make_nippo_data(nippo : str, eventId : ObjectId, purpose : str, chatlogId : ObjectId = None):
    print("make_nippo_data")
    print("nippo: ",nippo)

    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    db = client['mydb']

    # 削除パート
    collection = db['event']
    nippo_id = collection.find_one({"_id": eventId}).get("nippo_id", None)
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
        "event_time": event_time,
        "embedding": create_embedding(nippo, purpose)
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
    
    return nippo_id
