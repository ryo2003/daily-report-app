import os
import sys

from bson import ObjectId
import streamlit as st
import asyncio
from st_bridge import bridge, html
from pymongo import MongoClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/frontend/')))
from data_fetch import  init_database, fetch_async, get_username,get_client
from component_list import icon_toggle,icon_emb

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/frontend/')))
from component_list import hide_sidebar, hide_side_button
from dotenv import load_dotenv
load_dotenv()
mongo_URI = os.getenv("MONGO_URI")
client = MongoClient(mongo_URI)
db = client["mydb"]

hide_side_button()

def on_button_click():
    st.session_state['clicked'] = True
    st.write("Button was clicked!")

# Initialize session state
if 'clicked' not in st.session_state:
    st.session_state['clicked'] = False

async def main():
    # ログインしているユーザのid取得
    user_id = st.session_state.get("success_id")
    # 閲覧している日報のid取得(仮)
    nippo_id = st.session_state.get('selected_nippo_id', "66cfe05b8d90b8e8fead968b")

    
    filter = {
        "_id":nippo_id
    }
    # nippo_idからnippoデータを取得
    client = get_client()
    try:
        nippo = await fetch_async(filter)
    except:
        await init_database(client)
        nippo = await fetch_async(filter)
    
    # nippo_idの日報の作成者をユーザID取得
    print(nippo)
    author_id = nippo[0].user_id
    customer=nippo[0].customer
    event_time = nippo[0].event_time
    timestamp = nippo[0].timestamp
    purpose = nippo[0].purpose
    author_username = get_username(author_id)
    
    # nippo_idからeventidを取得して、イベント名を取得するコードを書く必要あり
    # 現在は仮のイベント名を入力
    event_name = customer + ": " + purpose
    iine_data = bridge(f"iine_{nippo_id}", default="")
    stock_data = bridge(f"stock_{nippo_id}", default="")

    contents = nippo[0].contents
    st.markdown(f"""
                <p class="h1">{event_name}</p>
        <div class="d-flex justify-content-between align-items-center">
        <div>
            <div class="d-flex">
            <i class="bi bi-person-circle mx-1"></i>
                <div class="mx-1">{author_username}</div>
            </div>
            <div class="d-flex">
            <i class="bi bi-building mx-1"></i>
                <div class="mx-1">{customer}</div>
            </div>
        </div>
</div>
""",unsafe_allow_html=True)
    html(f"""
                <div class="d-flex justify-content-between align-items-center">
    <div class="d-flex">
        <i class="bi bi-calendar mx-1 align-self-center"></i>
        <div>
            <div class="small mx-1">イベント時間：{event_time.strftime("%Y-%m-%d %H:%M:%S")}</div>
            <div class="small mx-1">日報作成日：{timestamp.strftime("%Y-%m-%d %H:%M:%S")}</div>
        </div>
    </div>
    <div class="d-flex">
    <div>
    {icon_toggle("hand-thumbs-up-fill",nippo_id,classes=["mx-1"],click_output="clicked",color="btn-outline-primary")}
    </div>

    <div>
    {icon_toggle("bookmark",nippo_id,classes=["mx-1"],click_output="clicked")}
    </div>
</div>
""")
   
    st.markdown("<hr>",unsafe_allow_html=True)
    st.write(contents)
    # カスタム評価ウィジェットの呼び出し
    if iine_data:
        st.write(iine_data)
        print("いいねが押されました")

    if stock_data:
        st.write(stock_data)
        print("ストックされました")
    
    if user_id == author_id:
        if st.button("編集する"):
            st.switch_page("pages/editpage.py")


    like = st.toggle("like")
    stock = st.toggle("stock")
    collection = db["nippo"]

    if user_id in collection.find_one({"_id": ObjectId(nippo_id)})["good"]:
        like = True
    
    if user_id in collection.find_one({"_id": ObjectId(nippo_id)})["bookmark"]:
        stock = True
    
    if like:
        new_likes = collection.find_one({"_id": ObjectId(nippo_id)})["good"]
        st.session_state["like"] = True
        new_likes.append(user_id)
        collection.update_one(
            {"_id": ObjectId(nippo_id)},
            {"$set": {"good": new_likes}}
        )

    else:
        new_likes = collection.find_one({"_id": ObjectId(nippo_id)})["good"]
        st.session_state["like"] = False
        new_likes.remove(user_id)
        collection.update_one(
            {"_id": ObjectId(nippo_id)},
            {"$set": {"good": new_likes}}
        )
    if stock:
        new_bookmarks = collection.find_one({"_id": ObjectId(nippo_id)})["bookmark"]
        st.session_state["stock"] = True
        new_bookmarks.append(user_id)
        collection.update_one(
            {"_id": ObjectId(nippo_id)},
            {"$set": {"bookmark": new_likes}}
        )
    else:
        new_bookmarks = collection.find_one({"_id": ObjectId(nippo_id)})["bookmark"]
        st.session_state["stock"] = False
        new_bookmarks.remove(ObjectId(user_id))

        collection.update_one(
            {"_id": ObjectId(nippo_id)},
            {"$set": {"bookmark": new_likes}}
        )

        
asyncio.run(main())