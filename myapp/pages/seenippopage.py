import streamlit as st
from bson import ObjectId
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))
from data_fetch import getnippo_from_nippoid, get_username
from streamlit_text_rating.st_text_rater import st_text_rater

#ログインしているユーザのid取得
userid = st.session_state.get("success_id")

#閲覧している日報のid取得(仮)
nippo_id = ObjectId("66cee55308302a8a9e19a148")

#nippo_idからnippoデータを取得
nippo = getnippo_from_nippoid(nippo_id)
#nippo_idの日報の作成者をユーザID取得
author_id = nippo["user_id"]
author_username = get_username(author_id)
#nippo_idからeventidを取得して、イベント名を取得するコードを書く必要あり
#現在は仮のイベント名を入力
event_name = "A会社との商談"

st.title(f"イベント:{event_name} の日報")
st.write(f"作成者: {author_username}")
contents = nippo["contents"]

# 情報をカード形式で表示
for key, value in contents.items():
    st.markdown(f"""
    <div style="background-color: #f5f5f5; border-radius: 10px; padding: 15px; margin-bottom: 10px;">
        <h4 style="margin: 0; color: #333;">{key}</h4>
        <p style="margin: 0; color: #666;">{value}</p>
    </div>
    """, unsafe_allow_html=True)

# もう少し見栄えを良くするためのカスタマイズ
st.markdown("""
    <style>
    .streamlit-expanderHeader {
        font-size: 1.5em;
        color: #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

for text in ["Is this text helpful?", "Do you like this text?"]:
    response = st_text_rater(text=text)
    # st.write(f"response --> {response}")
