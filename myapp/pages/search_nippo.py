import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))
from data_fetch import get_nippo, get_username, get_user, get_client, init_database, fetch_async
from bson import ObjectId
from st_bridge import bridge, html


# 仮の日報データ
# データベースができたらそっちから引っ張る
users = set()
customers = set()
purposes = set()

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

def get_attributes(nippos):
    for nippo in nippos:
        username = get_username(nippo.user_id)
        users.add(username)
        purpose = nippo.purpose
        purposes.add(purpose)
        customer = nippo.customer
        customers.add(customer)



def show_nippo(nippos):
    for nippo in nippos:  # Assuming nippos is your data
        username = get_username(nippo.user_id)
        purpose = nippo.purpose
        customer = nippo.customer
        src_time = nippo.timestamp
        nippo_id = nippo.id
        #st.write(nippo_id)
        
        # Store nippo_id in session state for each nippo when the link is clicked
        st.session_state[f'nippo_id_{nippo_id}'] = nippo_id

        # Initialize the bridge with a unique key for each iteration
        data = bridge(f"nippo-bridge-{nippo_id}", default="No button is clicked", key=f"bridge-key-{nippo_id}")

        # Define HTML with JavaScript to handle button clicks
        html(f"""
        <div style="background-color: whitesmoke; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
            <div style="font-size: 16px; color: dimgray;">Username: {username}</div>
            <div style="font-size: 16px; color: dimgray;">Purpose: {purpose}</div>
            <div style="font-size: 16px; color: dimgray;">Customer: {customer}</div>
            <div style="font-size: 12px; color: green;">{src_time}</div>
            <button style="margin-top: 10px; padding: 8px 16px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer;" 
                    onClick="stBridges.send('nippo-bridge-{nippo_id}', 'Nippo ID: {nippo_id}')">View Details</button>
        </div>
        """, key=f"html-key-{nippo_id}")

        # Display the data returned by the bridge (based on which button was clicked)
        #st.write(data)

        # Optionally, you can perform more logic depending on the returned data
        if "Nippo ID" in data:
            st.session_state['selected_nippo_id'] = nippo_id
            #st.success(f"Details fetched for {data}")
            st.switch_page("pages/nippo_detail.py") 

# Main async function to run the app
async def main():


    client = get_client()
    await init_database(client)
    
    nippo_data = await fetch_async()
    get_attributes(nippo_data)
    get_attributes(nippo_data)

    st.write("Nippo Data:")
    

    data = {
    "報告者": list(users),
    "企業名": list(customers),
    "訪問目的": list(purposes),
    }

    # 検索フォーム
    st.sidebar.header("検索条件")
    selected_name = st.sidebar.selectbox("報告者を選択してください", options=[None] + data.get("報告者"))
    selected_company = st.sidebar.selectbox("企業名を選択してください", options=[None] + data.get("企業名"))
    selected_purpose = st.sidebar.selectbox("訪問目的を選択してください", options=[None] + data.get("訪問目的"))
    #value = st.sidebar.slider('値を選択してください', 0, 100, 50)
    #st.write('選択した値は:', value)

    show_nippo(select_nippo(nippo_data,selected_name,selected_company,selected_purpose))
    

    # 検索フォーム
    st.sidebar.header("検索条件")
    selected_name = st.sidebar.selectbox("報告者を選択してください", options=[None] + data.get("報告者"))
    selected_company = st.sidebar.selectbox("企業名を選択してください", options=[None] + data.get("企業名"))
    selected_purpose = st.sidebar.selectbox("訪問目的を選択してください", options=[None] + data.get("訪問目的"))
    #value = st.sidebar.slider('値を選択してください', 0, 100, 50)
    #st.write('選択した値は:', value)

    show_nippo(select_nippo(nippo_data,selected_name,selected_company,selected_purpose))
    


# Entry point for the application
asyncio.run(main())


