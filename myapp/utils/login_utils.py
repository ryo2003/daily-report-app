import streamlit as st
import pymongo
from bson import ObjectId
from dotenv import load_dotenv
import os
load_dotenv()
mongo_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(mongo_URI)  # ここでURIを指定
db = client["mydb"]  # 使用するデータベース名
collection = db["user"]  # 使用するコレクション名

def check_loginid_exists(loginid):
    # クエリでloginidが存在するかを検索
    id_object = ObjectId(loginid)
    query = {"_id": id_object}
    result = collection.find_one(query)

    # 結果を判定
    if result:
        return True
    else:
        return False
    
def check_correctpassword(loginid,password):
    if check_loginid_exists(loginid):
        user = collection.find_one({"_id": ObjectId(loginid)})
        realpass = user.get("password")

        if realpass == password:
            return True
        else:
            return False
        
def login(login_id,password):

    try:
        check_loginid_exists(login_id)  
        #実際にはdb内にあるかを判定する

    except:
        st.error("ログインIDがデータベースに存在していません")

    else:
        if check_correctpassword(login_id,password):
            st.session_state["success_id"] = login_id
            st.success("ログイン成功!")
            st.switch_page("pages/toppage.py")
        else:
            st.error("ログインIDまたはパスワードが間違っています。")

