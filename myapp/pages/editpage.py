import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))
from data_register import submit_byhands_new,nippo_exist
from bson import ObjectId
from datetime import datetime
from bson import ObjectId
from models import Nippo
from pymongo import MongoClient
from data_fetch import fetch_async,get_client,init_database
import asyncio
mongo_URI = os.getenv("MONGO_URI")
client = MongoClient(mongo_URI)
db = client["mydb"]
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/frontend/')))
from component_list import hide_sidebar, hide_side_button

hide_side_button()

#ユーザid取得
userid = st.session_state.get("success_id")

async def main():

    # nippoid = st.session_state.get("justmade_nippo")
    client = get_client()

    await init_database(client)
    #仮データ！！！書き換えが必要
    nippoid = st.session_state.get("selected_nippo_id")

    nippo = await fetch_async(filter={"_id":nippoid},model=Nippo)
    nippo_data = nippo[0]
        # ヘッダー

    st.success("修正が必要な場合は、下記のフォームで修正してください。")
    st.title("日報データ編集フォーム")
    

    # 編集できない項目を表示
    st.write("### 日報詳細")
    st.text(f"企業名: {nippo_data.customer}")
    st.text(f"活動分類: {nippo_data.purpose}")
    st.text(f"投稿時間: {nippo_data.timestamp}")
    st.text(f"イベントの日時: {nippo_data.event_time}")



    # contentsの編集フォーム
    
    st.write("### 内容の編集")
    new_contents = st.text_area("本文", value=nippo_data.contents)
    new_contents += "(修正済)"

    if st.button("修正"):
        # 編集された内容を更新（保存処理は適宜実装）
        if userid != nippo_data.user_id:
            st.write("自分の作成した日報以外は編集できません")
        else:

            collection = db["nippo"]
            collection.update_one(
                {"_id": nippoid},
                {"$set": {"contents": new_contents}}
            )
            st.success("修正が保存されました。")

asyncio.run(main())