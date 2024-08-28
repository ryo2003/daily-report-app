import sys
import os

import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))

from chat import create_question, create_nippo, get_chatlog

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
        # チャットログを保存したセッション情報を初期化
        st.session_state.chat_log = []

        if st.session_state.chat_log == []:
            st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": "お疲れ様です。今回の営業の目的を教えてください。"})

    
        for chat in st.session_state.chat_log:
            print("chat",chat)
            print()
            avator = avator_img_dict.get(chat["name"], None)
            with st.chat_message(chat["name"]):
                st.write(chat["msg"])
        st.session_state.initialized = True

    
    user_msg = st.chat_input("ここにメッセージを入力!!!")

    if user_msg:
        # 以前のチャットログを表示
        for chat in st.session_state.chat_log:
            print("chat",chat)
            print()
            avator = avator_img_dict.get(chat["name"], None)
            with st.chat_message(chat["name"]):
                st.write(chat["msg"])
            

        if len(st.session_state.chat_log)//2 >= 3 or user_msg == "日報作成":
            assistant_msg=create_nippo(st.session_state.chat_log)
        else:
            assistant_msg=create_question(st.session_state.chat_log)

        with st.chat_message(USER_NAME):
            st.write(user_msg)
        with st.chat_message(ASSISTANT_NAME):
            st.write(assistant_msg)
        
        print("assistant_msg",assistant_msg)
        # セッションにチャットログを追加
        st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
        st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})
        print("st.session_state.chat_log",st.session_state.chat_log)

if __name__ == "__main__":
    main()