import sys
import os
import time
import streamlit as st
from bson import ObjectId

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))

from chat import create_question, create_nippo, get_chatlog, add_chatlog, pop_chatlog, make_nippo_data

def main():

    if st.session_state.get('event_data'):
        event_data = st.session_state['event_data']
        st.title(f"{event_data['title']}のチャットサンプル")
    else:
        st.title("NoEventチャットサンプル")
    # 定数定義
    USER_NAME = "user"
    ASSISTANT_NAME = "assistant"
    MORIAGE_YAKU_NAME ="moriage"

    avator_img_dict = {
        USER_NAME: "👤",
        ASSISTANT_NAME: "🤖",
        MORIAGE_YAKU_NAME: "🎉",
    }

    if 'initialized' not in st.session_state or not st.session_state.initialized:
        if 'chatlog_id' not in st.session_state or 'event_id' not in st.session_state:
            st.session_state.chatlog_id = ObjectId('66cd3e3a2dc71efad9fbd5df')
            st.session_state.event_id = ObjectId('66cd3a672dc71efad9fbd5de')
        
        print("st.session_state.chatlog_id",st.session_state.chatlog_id)
        print("get_chatlog(st.session_state.chatlog_id)",get_chatlog(st.session_state.chatlog_id))

        # チャットログを保存したセッション情報を初期化
        st.session_state.chat_log = get_chatlog(st.session_state.chatlog_id)

        if st.session_state.chat_log == []:
            assistant_msg = "お疲れ様です。今回の営業の目的を教えてください。"
            st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})
            add_chatlog(st.session_state.chatlog_id, {"name": ASSISTANT_NAME, "msg": assistant_msg})

    
        for chat in st.session_state.chat_log:
            print("chat",chat)
            print()
            avator = avator_img_dict.get(chat["name"], None)
            with st.chat_message(chat["name"]):
                st.write(chat["msg"])
        st.session_state.initialized = True
    
    with st.sidebar:
        st.title("にっぽー")
        make_nippo = st.button("日報作成")
        save_nippo = st.button("日報を保存する")

    
    user_msg = st.chat_input("ここにメッセージを入力! 日報を作成したいときは「日報作成」と入力してください。")

    if save_nippo:
        user_msg = "日報を保存。"
        make_nippo_data(st.session_state.chat_log[-1]['msg'], st.session_state.event_id, "営業", st.session_state.chatlog_id)
        assistant_msg = "日報を保存しました。"

    elif make_nippo:
        user_msg = "日報作成"
        if len(st.session_state.chat_log) < 2:
            assistant_msg = "コンテンツがありません"
        else:
            print("st.session_state.chat_log",st.session_state.chat_log)
            assistant_msg=create_nippo(st.session_state.chat_log[:-1])
            st.session_state.chat_log.pop()
            pop_chatlog(st.session_state.chatlog_id)
            print("st.session_state.chat_log",st.session_state.chat_log)
    
    elif user_msg:
        assistant_msg=create_question(st.session_state.chat_log)

    if user_msg or make_nippo or save_nippo:
        # 以前のチャットログを表示
        for chat in st.session_state.chat_log:
            print("chat",chat)
            avator = avator_img_dict.get(chat["name"], None)
            with st.chat_message(chat["name"]):
                st.write(chat["msg"])
                

        with st.chat_message(USER_NAME):
            st.write(user_msg)
        with st.chat_message(ASSISTANT_NAME):
            st.write(assistant_msg)
        
        print("assistant_msg",assistant_msg)
        # セッションにチャットログを追加
        st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
        st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})
        print("st.session_state.chat_log",st.session_state.chat_log)
        add_chatlog(st.session_state.chatlog_id, {"name": USER_NAME, "msg": user_msg})
        add_chatlog(st.session_state.chatlog_id, {"name": ASSISTANT_NAME, "msg": assistant_msg})

if __name__ == "__main__":
    main()

