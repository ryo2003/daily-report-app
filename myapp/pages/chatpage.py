import sys
import os
import time
import streamlit as st
from bson import ObjectId
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))

from chat import create_question, create_nippo, add_chatlog, \
pop_chatlog, make_nippo_data, extract_keys_from_json, \
add_catdata, reset_log, get_data

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/frontend/')))
from component_list import hide_sidebar, hide_side_button

hide_side_button()


# 定数定義
USER_NAME = "user"
ASSISTANT_NAME = "assistant"
MORIAGE_YAKU_NAME ="moriage"


avator_img_dict = {
    USER_NAME: "👤",
    ASSISTANT_NAME: "🤖",
    MORIAGE_YAKU_NAME: "🎉",
}


def page():
    if st.session_state.get('event_data'):
        event_data = st.session_state['event_data']
        st.title(f"{event_data['customer']}の日報作成チャット")
    else:
        st.title("NoEventの日報作成チャット")

    if not st.session_state.nippo_cat:
        cat = st.selectbox(
            "日報のカテゴリを選択してください", 
            st.session_state.report_class,
            index = None,
            placeholder="日報のカテゴリを選択してください"
            )
        print("cat",cat)
        
        if cat:
            st.session_state.nippo_cat = cat
            print("st.session_state.nippo_cat",st.session_state.nippo_cat)
            add_catdata(st.session_state.chatlog_id, cat)
            with st.chat_message(ASSISTANT_NAME):
                st.write(f"日報のカテゴリを{cat}に設定しました。")
            st.rerun()
    
    if st.session_state.nippo_cat:
        st.write(f"日報のカテゴリは{st.session_state.nippo_cat}です。")
        for chat in st.session_state.chat_log:
            print("chat",chat)
            avator = avator_img_dict.get(chat["name"], None)
            with st.chat_message(chat["name"]):
                st.write(chat["msg"])
        print("end chat")


def main():
    if 'initialized_chatpage' not in st.session_state or not st.session_state.initialized_chatpage:
        
        st.session_state.report_class = extract_keys_from_json("report_category.json")
        print("st.session_state.report_class",st.session_state.report_class)

        if 'event_id' not in st.session_state:
            st.session_state.event_id = ObjectId('66cd3a672dc71efad9fbd5de')
        else:
            st.session_state.event_id = ObjectId(st.session_state.event_id)
        
        print("st.session_state.event_id",st.session_state.event_id, type(st.session_state.event_id))
        data = get_data(st.session_state.event_id)
        
        st.session_state.event_data = data["event"]
        st.session_state.chatlog_id = data["chatlog_id"]
        st.session_state.chat_log = data["chatlog"]
        st.session_state.nippo_cat = data["category"]

        print(data)
        print("st.session_state.event_data",st.session_state.event_data)
        print("st.session_state.chatlog_id",st.session_state.chatlog_id)
        print("st.session_state.chat_log",st.session_state.chat_log)
        print("st.session_state.nippo_cat",st.session_state.nippo_cat)

        if st.session_state.chat_log == []:
            assistant_msg = "お疲れ様です。今回の営業で同行者はいましたか？"
            st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})
            add_chatlog(st.session_state.chatlog_id, {"name": ASSISTANT_NAME, "msg": assistant_msg})
        
        st.session_state.next_chat = USER_NAME if st.session_state.chat_log[-1]["name"] == ASSISTANT_NAME else ASSISTANT_NAME
        
        st.session_state.initialized_chatpage = True
        
    page()
    
    with st.sidebar:
        st.title("にっぽー")
        make_nippo = st.button("日報作成")
        save_nippo = st.button("日報を保存する")
        reset = st.button("リセット")
    
    if reset:
        st.session_state.chat_log = []
        reset_log(st.session_state.chatlog_id, st.session_state.event_data.get("purpose"))
        assistant_msg = "お疲れ様です。今回の営業で同行者はいましたか？"
        st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})
        add_chatlog(st.session_state.chatlog_id, {"name": ASSISTANT_NAME, "msg": assistant_msg})
        st.session_state.next_chat = USER_NAME
        st.rerun()
    
    if st.session_state.next_chat == USER_NAME:
        user_msg = st.chat_input("ここにメッセージを入力!")

        if user_msg or make_nippo or save_nippo:
            if save_nippo:
                with st.chat_message(ASSISTANT_NAME):
                    st.success("日報を保存しました。")
                nippoId = make_nippo_data(st.session_state.chat_log[-1]['msg'], st.session_state.event_id, st.session_state.nippo_cat, st.session_state.chatlog_id)
                st.session_state.nippo_justmade = nippoId
                # st.switch_page("pages/editpage.py")


            elif make_nippo:
                if len(st.session_state.chat_log) < 2:
                    with st.chat_message(ASSISTANT_NAME):
                        st.warning("コンテンツがありません")
                else:
                    user_msg = "日報作成"
                    with st.chat_message(USER_NAME):
                        st.write(user_msg)

                    print("st.session_state.chat_log",st.session_state.chat_log)
                    st.session_state.chat_log.pop()
                    pop_chatlog(st.session_state.chatlog_id)
                    if st.session_state.chat_log[-1]["msg"] == "日報作成":
                        st.session_state.chat_log.pop()
                        pop_chatlog(st.session_state.chatlog_id)
                    print("st.session_state.chat_log",st.session_state.chat_log)
                    
                    assistant_msg = create_nippo(st.session_state.chat_log, st.session_state.event_data)
                    print("assistant_msg",assistant_msg)
                    st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
                    st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})
                    add_chatlog(st.session_state.chatlog_id, {"name": USER_NAME, "msg": user_msg})
                    add_chatlog(st.session_state.chatlog_id, {"name": ASSISTANT_NAME, "msg": assistant_msg})
                    st.rerun()

            else:
                st.session_state.chat_log.append({"name": USER_NAME, "msg": user_msg})
                add_chatlog(st.session_state.chatlog_id, {"name": USER_NAME, "msg": user_msg})
                st.session_state.next_chat = ASSISTANT_NAME
                with st.chat_message(USER_NAME):
                    st.write(user_msg)
                st.rerun()

    else:
        assistant_msg = create_question(st.session_state.chat_log, st.session_state.event_data)
        st.session_state.chat_log.append({"name": ASSISTANT_NAME, "msg": assistant_msg})
        add_chatlog(st.session_state.chatlog_id, {"name": ASSISTANT_NAME, "msg": assistant_msg})
        st.session_state.next_chat = USER_NAME
        st.rerun()

main()

