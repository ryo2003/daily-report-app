import streamlit as st

st.set_page_config(page_title="Streamlit App", page_icon=":shark:")

top_page = st.Page(page="pages/toppage.py", title="Top", icon=":material/home:")
my_profile = st.Page(page="pages/mypage.py", title="mypage", icon=":material/calendar_month:")
search = st.Page(page="pages/search_nippo.py", title="search", icon=":material/manage_search:")
chat = st.Page(page="pages/chatpage.py", title="chat", icon=":material/home:")
create_by_hand = st.Page(page="pages/createbyhands.py",title = "手動で日報作成",)
login = st.Page(page="pages/login.py",title = "login")
event = st.Page(page="pages/Event.py",title = "event")
seenippo = st.Page(page="pages/nippo_detail.py",title="日報詳細閲覧ページ",icon=":material/visibility:")
seemynippo = st.Page(page="pages/seemynippo.py",title="自分の日報",icon=":material/visibility:")
css="""
<style>
    [data-testid="stForm"] {
        background: LightBlue;
    }
</style>
"""
st.write(css, unsafe_allow_html=True)
st.markdown("""
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz" crossorigin="anonymous"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.0/font/bootstrap-icons.css">
            """,unsafe_allow_html=True)
pg = st.navigation([top_page, my_profile,search,chat,create_by_hand,login,event,seenippo,seemynippo])
pg.run()