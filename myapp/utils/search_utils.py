import os
import sys
import streamlit as st
import pandas as pd
from bson import ObjectId
from st_bridge import bridge, html

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/frontend/')))
from data_fetch import get_nippo, get_username, get_user, get_client, init_database, fetch_async
from component_list import nippo_card
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


def show_nippo(nippos,sort_type=None):#sort_type = "newest", "oldest", "most_likes"
    iine_dict = {}
    stock_dict = {}
    if sort_type:
        nippos = sort_nippo(nippos,sort_type)
    for nippo in nippos:  # Assuming nippos is your data
        username = get_username(nippo.user_id)
        purpose = nippo.purpose
        customer = nippo.customer
        src_time = nippo.timestamp
        nippo_id = nippo.id
        contents = nippo.contents
        #st.write(nippo_id)
        
        # Store nippo_id in session state for each nippo when the link is clicked
        st.session_state[f'nippo_id_{nippo_id}'] = nippo_id

        # Initialize the bridge with a unique key for each iteration
        data = bridge(f"nippo-bridge-{nippo_id}", default="No button is clicked", key=f"bridge-key_{nippo_id}")
        # iine_dict[nippo_id]=bridge(f"hand-thumbs-up-fill_{nippo_id}", default="", key=f"bridge-key_i_{nippo_id}")
        # stock_dict[nippo_id]=bridge(f"bookmark_{nippo_id}", default="", key=f"bridge-key_s_{nippo_id}")
        # Define HTML with JavaScript to handle button clicks
        html_tem = nippo_card(username,purpose,customer,src_time,nippo_id,contents)
        html(html_tem, key=f"html-key-{nippo_id}")

        # Display the data returned by the bridge (based on which button was clicked)
        #st.write(data)

        # Optionally, you can perform more logic depending on the returned data
        
        if "Nippo ID" in data:
            st.session_state['selected_nippo_id'] = nippo_id
            #st.success(f"Details fetched for {data}")
            st.switch_page("pages/nippo_detail.py") 
        
def sort_nippo(nippos,sort_type="newest"):
    if sort_type == "新しい順":
        sort_type = "newest"
    elif sort_type == "古い順":
        sort_type = "oldest"
    elif sort_type == "いいねが多い順":
        sort_type = "most_likes"
    sorted_list = sorted(nippos,key=lambda x: x.timestamp, reverse=True)
    if(sort_type == "oldest"):
        sorted_list = sorted(nippos,key=lambda x: x.timestamp)
    return sorted_list