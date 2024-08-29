import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))
from data_register import submit_byhands_new
from bson import ObjectId
from datetime import datetime

userid = st.session_state.get("success_id")

event_data = st.session_state.get("event_data")
company_name = event_data["title"]
visit_time = event_data["start"]


# ページのタイトル
st.title("日報作成")

# 企業名
st.write("会社名:{}".format(company_name))

# 訪問時間
st.write("訪問時間:{}".format(visit_time))

# 訪問目的
visit_purpose = st.selectbox(
    "訪問目的",
    [ "電話対応","提案・見積もり","CS訪問","ヒアリング","納品","クロージング", "その他"]
)

# 本文
customer_issues = st.text_area("本文を入力してください。お客様の課題・同行者・次回訪問などがある場合、それも記入してください。", height=100)


nippo_temporary = {"企業名":company_name,"訪問時間":format(visit_time),"訪問目的":visit_purpose,"本文":customer_issues}

if st.button("確認"):
    st.session_state['getconsent'] = True
    st.session_state['nippo_temp'] = nippo_temporary

if st.session_state.get('getconsent'):
    if not nippo_temporary["企業名"]:
        st.write("企業名を入力してください")
    else:
            
        st.write("以下の内容を本当に送信しますか？")
        st.write(f"企業名: {nippo_temporary['企業名']}")
        st.write(f"訪問時間: {nippo_temporary['訪問時間']}")
        st.write(f"訪問目的: {nippo_temporary['訪問目的']}")
        st.write(f"本文: {nippo_temporary['本文']}")


        if st.button("送信する"):
            submit_byhands_new(nippo_temporary,userid,event_data)
            st.write("送信しました")
