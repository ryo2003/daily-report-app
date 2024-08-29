import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))
from data_fetch import get_nippo, get_username, get_user, get_client, init_database, fetch_async
from bson import ObjectId

# 仮の日報データ
# データベースができたらそっちから引っ張る
users = []
customers = []
purposes = []

st.title("日報検索")

st.title("Feed View Example")

import streamlit as st
import asyncio
def select_nippo(nippos,sel_username=None,sel_customer=None, sel_purpose=None):
    selected_nippo = []

    for nippo in nippos:
        # Check if sel_username is provided and matches the nippo's username
        if sel_username and get_username(nippo.user_id) != sel_username:
            continue
        
        # Check if sel_customer is provided and matches the nippo's customer
        if sel_customer and nippo.customer != sel_customer:
            continue

        if sel_purpose and nippo.purpose != sel_purpose:
            continue
        
        # If all provided conditions are met, add the nippo to the selected list
        selected_nippo.append(nippo)
    return selected_nippo
            


def show_nippo(nippos):
    result_str = '<html><table style="border: none; width: 100%;">'
    
    for nippo in nippos:
        username = get_username(nippo.user_id)
        users.append(username)
        purpose = nippo.purpose
        purposes.append(purpose)
        customer = nippo.customer
        customers.append(customer)
        src_time = nippo.get("src_time", "Unknown time")
        
        result_str += f'<tr style="border: none; background-color: whitesmoke; margin-bottom: 15px;">'
        result_str += f'<td style="border: none; padding: 10px;">'

        # Display username
        result_str += f'<div style="font-size: 16px; color: dimgray; margin-top: 5px;">Username: {username}</div>'
        
        
        # Display purpose
        result_str += f'<div style="font-size: 16px; color: dimgray; margin-top: 5px;">Purpose: {purpose}</div>'
        
        # Display customer
        result_str += f'<div style="font-size: 16px; color: dimgray; margin-top: 5px;">Customer: {customer}</div>'
        
        # Display time
        result_str += f'<div style="font-size: 12px; color: green; margin-top: 10px;">{src_time}</div>'
        
        result_str += f'</td></tr>'
        
        # Spacer row
        result_str += f'<tr style="border: none;"><td style="border: none; height: 10px;"></td></tr>'

    result_str += '</table></html>'

    # Hide Streamlit's menu and footer
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .css-hi6a2p {padding-top: 0rem;}
        </style>
        """

    # Render the result in Streamlit
    st.markdown(result_str, unsafe_allow_html=True)
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Main async function to run the app
async def main():

    client = get_client()
    await init_database(client)
    
    nippo_data = await fetch_nippo_async()

    st.write("Nippo Data:")
    

    #st.write(users)

    data = {
    "報告者": ["users","su","c"],
    "企業名": ["Project Planning","HIJ株式会社","c"],
    "訪問時間": ["2024-08-20 10:00", "2024-08-21 14:00", "2024-08-22 09:00"],
    "訪問目的": ["価格競争が激しい", "納期の短縮", "競合他社が強力"],
    "お客様の課題": ["価格競争が激しい", "納期の短縮", "競合他社が強力"],
    }

    # 検索フォーム
    st.sidebar.header("検索条件")
    selected_name = st.sidebar.selectbox("報告者を選択してください", options=[None] + data.get("報告者"))
    selected_company = st.sidebar.selectbox("企業名を選択してください", options=[None] + data.get("企業名"))
    selected_purpose = st.sidebar.selectbox("訪問目的を選択してください", options=[None] + data.get("訪問目的"))
    value = st.sidebar.slider('値を選択してください', 0, 100, 50)
    st.write('選択した値は:', value)

    # 検索ボタン
    search_button = st.sidebar.button("検索")

    show_nippo(select_nippo(nippo_data,selected_name,selected_company))

    #selected_name/company/purposeをutilsの検索functionに入れる
    if search_button :
        st.write("報告者："+selected_name+" 企業名："+selected_company+" 訪問目的:"+selected_purpose+"　での検索結果は以下です")
        st.write("まだ検索用の関数が作られていないためエラーがでます")
        #select_nippo(nippo_data,selected_name)
        #search_result = utils.search(selected_name,selected_company,selected_purpose)
        #st.write(search_result)
    


# Entry point for the application
asyncio.run(main())

