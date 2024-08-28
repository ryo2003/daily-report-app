import streamlit as st


if st.session_state.get("success_id"):
    userid = st.session_state.get("success_id")
    st.write("お疲れ様です、"+userid+"さん。日報管理システムへようこそ!")


if st.button("マイページ"):
    # クエリパラメータを設定して、search.pyページに遷移
    st.switch_page("pages/mypage.py")

if st.button("日報検索ページ"):
    # クエリパラメータを設定して、search.pyページに遷移
    st.switch_page("pages/search_nippo.py")