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


import streamlit as st
from st_bridge import bridge, html

data = bridge("nippo-bridge", default="No button is clicked")

# Define HTML with JavaScript to handle button clicks
html(f"""
<div style="background-color: whitesmoke; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
    <div style="font-size: 16px; color: dimgray;">Username: ayachan</div>
    <div style="font-size: 16px; color: dimgray;">Purpose: 提案・見積もり</div>
    <div style="font-size: 16px; color: dimgray;">Customer: PQR株式会社</div>
    <div style="font-size: 12px; color: green;">2024-08-29 03:33:31.812000</div>
    <button style="margin-top: 10px; padding: 8px 16px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;" 
            onClick="stBridges.send('nippo-bridge', 'Nippo ID: 66cfdb1c49886065db244707')">View Details</button>
</div>
""")

# Display the data returned by the bridge (based on which button was clicked)
st.write(data)

# Optionally, you can perform more logic depending on the returned data
if "Nippo ID" in data:
    st.success(f"Details fetched for {data}")