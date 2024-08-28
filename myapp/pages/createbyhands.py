import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))
from data_register import submit_byhands

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

# 同行者名
companion_name = st.text_input("同行者名")

# お客様の課題
customer_issues = st.text_area("お客様の課題", height=100)

# 次回訪問日程
next_visit_schedule = st.date_input("次回訪問日程")

# 次回訪問目的
next_visit_purpose = st.selectbox(
    "次回訪問目的",
    ["選択してください", "初回訪問", "精査", "提案", "クローズ", "関係構築", "フォロー", "納品","その他"]
)

nippo_temporary = {"企業名":company_name,"訪問時間":visit_time,"訪問目的":visit_purpose,"同行者名":companion_name,"お客様の課題":customer_issues,"次回訪問日程":next_visit_schedule,"次回訪問目的":next_visit_purpose}

nippo_containts = "企業名:"+nippo_temporary['企業名']+"訪問時間:+nippo_temporary['訪問時間']"+"訪問目的: "+nippo_temporary['訪問目的']+"同行者名: "+nippo_temporary['同行者名']+"お客様の課題:"+nippo_temporary['お客様の課題']+"次回訪問日程:+nippo_temporary['次回訪問日程']"
submit_data = {"企業名":company_name,"訪問目的":visit_purpose,"内容":nippo_containts}
if st.button("送信"):
    st.session_state['getconsent'] = True
    st.session_state['event_data'] = nippo_temporary

if st.session_state.get('getconsent'):
    if not nippo_temporary["企業名"]:
        st.write("企業名を入力してください")
    else:
            
        st.write("以下の内容を本当に送信しますか？")
        st.write(f"企業名: {nippo_temporary['企業名']}")
        st.write(f"訪問時間: {nippo_temporary['訪問時間']}")
        st.write(f"訪問目的: {nippo_temporary['訪問目的']}")
        st.write(f"同行者名: {nippo_temporary['同行者名']}")
        st.write(f"お客様の課題: {nippo_temporary['お客様の課題']}")
        st.write(f"次回訪問日程: {nippo_temporary['次回訪問日程']}")

        if st.button("送信する"):
            submit_byhands(submit_data)
            st.write("送信しました")