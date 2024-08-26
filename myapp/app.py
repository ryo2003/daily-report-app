import streamlit as st

st.set_page_config(page_title="Streamlit App", page_icon=":shark:")


top_page = st.Page(page="pages/toppage.py", title="Top", icon=":material/home:")
my_profile = st.Page(page="pages/mypage.py", title="mypage", icon=":material/open_with:")
search = st.Page(page="pages/search_nippo.py", title="search", icon=":material/home:")
chat = st.Page(page="pages/chatpage.py", title="chat", icon=":material/home:")
create_by_hand = st.Page(page="pages/createbyhands.py",title = "手動で日報作成")
pg = st.navigation([top_page, my_profile,search,chat,create_by_hand])
pg.run()