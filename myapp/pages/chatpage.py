import sys
import os

import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))

from chat import create_question


if st.session_state.get('event_data'):
    event_data = st.session_state['event_data']
    st.title(f"{event_data['title']}のチャットサンプル")
else:
    st.title("NoEventチャットサンプル")
# 定数定義
USER_NAME = "user"
ASSISTANT_NAME = "assistant"
MORIAGE_YAKU_NAME ="moriage"
# チャットログを保存したセッション情報を初期化
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

# ユーザーのアバターを設定
avator_img_dict = {
    MORIAGE_YAKU_NAME: "🎉",
}

user_msg = st.chat_input("ここにメッセージを入力")

if user_msg:
    # 以前のチャットログを表示
    for chat in st.session_state.chat_log:
        avator = avator_img_dict.get(chat["name"], None)
        with st.chat_message(chat["name"], avatar=avator):
            st.write(chat["msg"])

    assistant_msg=create_question("",user_msg)
    with st.chat_message(USER_NAME):
        st.write(user_msg)
    with st.chat_message(ASSISTANT_NAME):
        st.write(assistant_msg)

    # セッションにチャットログを追加
    st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
    st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": user_msg})