import streamlit as st
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))
from data_fetch import get_username

if st.session_state.get("success_id"):
    userid = st.session_state.get("success_id")
    username = get_username(userid)
    st.write("お疲れ様です、"+username+"さん。日報管理システムへようこそ!")


if st.button("マイページ"):
    # クエリパラメータを設定して、search.pyページに遷移
    st.switch_page("pages/mypage.py")

if st.button("日報検索ページ"):
    # クエリパラメータを設定して、search.pyページに遷移
    st.switch_page("pages/search_nippo.py")