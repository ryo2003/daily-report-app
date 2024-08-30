import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))
from data_fetch import get_nippo, get_username, get_user, get_client, init_database, fetch_async
from bson import ObjectId
from search_utils import select_nippo, get_attributes,show_nippo
import asyncio

# 仮の日報データ
# データベースができたらそっちから引っ張る

myid = st.session_state.get("success_id")
myname = get_username(myid)
st.title("{}さんの日報".format(myname))

users = set()
customers = set()
purposes = set()

# Main async function to run the app
async def main():

    client = get_client()
    await init_database(client)
    
    nippo_data = await fetch_async()
    get_attributes(nippo_data)

    st.write("Nippo Data:")
    

    data = {
    "報告者": list(users),
    "企業名": list(customers),
    "訪問時間": ["2024-08-20 10:00", "2024-08-21 14:00", "2024-08-22 09:00"],
    "訪問目的": list(purposes),
    "お客様の課題": ["価格競争が激しい", "納期の短縮", "競合他社が強力"],
    }

    # 検索フォーム
    st.sidebar.header("検索条件")
    selected_name = myname
    selected_company = st.sidebar.selectbox("企業名を選択してください", options=[None] + data.get("企業名"))
    selected_purpose = st.sidebar.selectbox("訪問目的を選択してください", options=[None] + data.get("訪問目的"))
    value = st.sidebar.slider('値を選択してください', 0, 100, 50)
    st.write('選択した値は:', value)

    show_nippo(select_nippo(nippo_data,selected_name,selected_company,selected_purpose))


    



# Entry point for the application
asyncio.run(main())
