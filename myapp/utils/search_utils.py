import streamlit as st
import asyncio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))
from data_fetch import get_nippo, get_username, get_user, get_client, init_database, fetch_async
from bson import ObjectId

users = set()
customers = set()
purposes = set()

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
    result_str = '<html><table style="border: none; width: 100%;">'
    
    for nippo in nippos:
        username = get_username(nippo.user_id)
        users.add(username)
        purpose = nippo.purpose
        purposes.add(purpose)
        customer = nippo.customer
        customers.add(customer)
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
