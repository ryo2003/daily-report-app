import streamlit as st

st.title("Streamlitのチャットサンプル")

# 定数定義
USER_NAME = "user"
ASSISTANT_NAME = "assistant"
MORIAGE_YAKU_NAME = "moriage_yaku"

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

    # 最新のメッセージを表示
    assistant_msg = "もう一度入力してください"
    with st.chat_message(USER_NAME):
        st.write(user_msg)
    with st.chat_message(ASSISTANT_NAME):
        st.write(assistant_msg)

    # セッションにチャットログを追加
    st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
    st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": user_msg})
    st.session_state.chat_log.append({"name": MORIAGE_YAKU_NAME, "msg": user_msg})