import os
import sys

from bson import ObjectId
import streamlit as st
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))
from data_fetch import  init_database, fetch_async, get_username,get_client
from streamlit_text_rating.st_text_rater import st_text_rater


async def main():
    # ログインしているユーザのid取得
    user_id = st.session_state.get("success_id")
    # 閲覧している日報のid取得(仮)
    nippo_id = st.session_state.get('selected_nippo_id', None)

    
    filter = {
        "_id":nippo_id
    }
    # nippo_idからnippoデータを取得
    client = get_client()
    await init_database(client)
    nippo = await fetch_async(filter)
    # nippo_idの日報の作成者をユーザID取得
    author_id = nippo[0].user_id
    author_username = get_username(author_id)

    # nippo_idからeventidを取得して、イベント名を取得するコードを書く必要あり
    # 現在は仮のイベント名を入力
    event_name = "A会社との商談"

    contents = nippo[0].contents


    st.title(f"イベント: {event_name} の日報")
    st.write(f"作成者: {author_username}")
    st.write(contents)
    # カスタム評価ウィジェットの呼び出し
    text = "この日報は役に立ちましたか？"
    response = st_text_rater(text=text)
    # セッション状態の更新
    if response == "liked":
        st.session_state["response"] = response
    elif response == "disliked":
        st.session_state["response"] = response

    # ボタンが押されたらメッセージを表示
    if st.session_state.get("response") == "liked":
        st.write("いいねしました")
    elif st.session_state.get("response") == "disliked":
        st.write("バッドしました")

asyncio.run(main())