import streamlit as st
import pymongo
from dotenv import load_dotenv
import os
import sys
load_dotenv()
mongo_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(mongo_URI)  # ここでURIを指定
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))
from data_fetch import get_id_from_username

db = client["mydb"]  # 使用するデータベース名
collection = db["user"]  # 使用するコレクション名

def check_username_exists(username):
    # クエリでloginidが存在するかを検索
    query = {"user_name": username}
    result = collection.find_one(query)

    # 結果を判定
    if result:
        return True
    else:
        return False
    
def check_correctpassword(username,password):
    if check_username_exists(username):
        user = collection.find_one({"user_name":username})
        realpass = user.get("password")

        if realpass == password:
            return True
        else:
            return False
        
def login(username,password):

    try:
        check_username_exists(username)  

    except:
        st.error("ユーザがデータベースに存在していません")

    else:
        if check_correctpassword(username,password):
            st.session_state["success_id"] = get_id_from_username(username)
            st.success("ログイン成功!")
            st.switch_page("pages/toppage.py")
        else:
            st.error("ユーザ名またはパスワードが間違っています。")

