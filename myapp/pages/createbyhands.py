import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))
from data_register import submit_byhands_new

userid = st.session_state.get("success_id")
# ページのタイトル
st.title("日報作成")

# 企業名
company_name = st.text_input("企業名")

# 訪問時間
visit_time = st.date_input("訪問時間")

# 訪問目的
visit_purpose = st.selectbox(
    "訪問目的",
    ["選択してください", "初回訪問", "精査", "提案", "クローズ", "関係構築", "フォロー", "納品"]
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
            submit_byhands_new(userid,st.session_state.get["nippo_temp"])
            st.write("送信しました")