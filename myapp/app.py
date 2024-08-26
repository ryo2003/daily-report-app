import streamlit as st

st.set_page_config(page_title="Streamlit App", page_icon=":shark:")


top_page = st.Page(page="pages/toppage.py", title="Top", icon=":material/home:")
my_profile = st.Page(page="pages/mypage.py", title="mypage", icon=":material/open_with:")
search = st.Page(page="pages/search_nippo.py", title="search", icon=":material/home:")
chat = st.Page(page="pages/chatpage.py", title="chat", icon=":material/home:")
pg = st.navigation([top_page, my_profile,search,chat])
pg.run()