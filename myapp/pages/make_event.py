import streamlit as st
import sys
import os
import asyncio
from datetime import datetime

from bson import ObjectId
from pymongo import MongoClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/mount/src/nippo/myapp/utils/')))
from data_register import submit_byhands_new,nippo_exist,insert_event
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/mount/src/nippo/myapp/frontend/')))
from component_list import hide_sidebar, hide_side_button

hide_side_button()

mongo_URI = st.secrets["MONGO_URI"]
client = MongoClient(mongo_URI)
db = client["mydb"]
events = db["event"]
userid = st.session_state.get("success_id")



# フォームの作成
with st.form("event_form"):
    # 顧客名の入力
    time_9_am = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    time_18 = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)
    company_name = st.text_input("顧客名", placeholder="例: ダミー株式会社")
    
    # イベントの開始時間の入力
    start_date = st.date_input("開始日", value=datetime.now(),key="startd_date")
    start_time = st.time_input("開始時間",value=time_9_am,key="start_time")
    start_datetime = datetime.combine(start_date,start_time)
    
    # イベントの終了時間の入力
    end_date = st.date_input("開始日",value=datetime.now(),key="end_date")
    end_time = st.time_input("終了時間",value=time_18,key="end_time")
    end_datetime = datetime.combine(end_date,end_time)
    # 住所の入力
    address = st.text_input("住所", placeholder="例: 東京都千代田区1-1-1")
    
    # 目的の入力
    purpose_options = [
    "電話対応",
    "提案・見積もり",
    "CS訪問",
    "ヒアリング",
    "納品",
    "クロージング",
    "その他"
    ]   

# セレクトボックスの作成
    purpose = st.selectbox("対応内容を選択してください:", purpose_options)
    
    # 送信ボタン
    submitted = st.form_submit_button("送信")

    if submitted:
    # 入力データの表示
        st.write("### 入力されたデータ")
        st.write(f"顧客名: {company_name}")
        st.write(f"開始時間: {start_datetime}")
        st.write(f"終了時間: {end_datetime}")
        st.write(f"住所: {address}")
        st.write(f"目的: {purpose}")

        insert_event(userid, company_name, start_datetime, end_datetime, address, purpose)
