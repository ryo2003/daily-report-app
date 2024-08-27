import streamlit as st

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
    ["選択してください", "初回訪問", "精査", "提案", "クローズ", "関係構築", "フォロー", "納品"]
)