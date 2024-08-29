import streamlit as st
from bson import ObjectId
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))
from data_fetch import getnippo_from_nippoid, get_username
from streamlit_text_rating.st_text_rater import st_text_rater

# ログインしているユーザのid取得
userid = st.session_state.get("success_id")

# 閲覧している日報のid取得(仮)
nippo_id = ObjectId("66cee55308302a8a9e19a148")

# nippo_idからnippoデータを取得
nippo = getnippo_from_nippoid(nippo_id)

# nippo_idの日報の作成者をユーザID取得
author_id = nippo["user_id"]
author_username = get_username(author_id)

# nippo_idからeventidを取得して、イベント名を取得するコードを書く必要あり
# 現在は仮のイベント名を入力
event_name = "A会社との商談"

st.title(f"イベント: {event_name} の日報")
st.write(f"作成者: {author_username}")
contents = nippo["contents"]

# シンプルな列挙形式で表示
st.subheader("日報の内容")
for key, value in contents.items():
    st.write(f"- **{key}**: {value}")

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

