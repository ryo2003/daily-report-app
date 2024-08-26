import streamlit as st

st.title("お疲れ様です。日報管理システムへようこそ！")


if st.button("マイページ"):
    # クエリパラメータを設定して、search.pyページに遷移
    st.switch_page("pages/mypage.py")

if st.button("日報検索ページ"):
    # クエリパラメータを設定して、search.pyページに遷移
    st.switch_page("pages/search_nippo.py")