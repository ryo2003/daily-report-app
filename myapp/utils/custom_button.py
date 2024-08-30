import streamlit as st
from st_bridge import bridge, html

def toggle(col):
    col= "white" if col=="blue" else "blue"
    print(col)
    return col

def iine_button(id):
    if not st.session_state.get("iine"):
        st.session_state["iine"]={}
    
    if  st.session_state["iine"].get(id):
        color=st.session_state["iine"][id]
    else:
        color="white"
        st.session_state["iine"][id]=color
    data = bridge("iine_{id}", default="no button is clicked")
    html(f"""
    <button onClick="stBridges.send('iine_{id}', 'clicked')"></button>
    """)
    if data:
        color=toggle(color)
        st.session_state["iine"][id]=color



def stock_button(id):
    if not st.session_state.get("stock"):
        st.session_state["stock"]={}
    
    if  st.session_state["stock"].get(id):
        color=st.session_state["stock"][id]
    else:
        color="white"
        st.session_state["stock"][id]=color
    data = bridge(f"stock_{id}", default="no button is clicked")
    html(f"""
    <button onClick="stBridges.send('stock_{id}', 'clicked')">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color={color}>
        <path d="M4 4h16v16H4V4zm0-2C2.9 2 2 2.9 2 4v16c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2H4zm12 11.2l-4.8 2.4V8h1.6v5.8l3.2-1.6v1.4z" fill="#000"/>
        </svg>
    </button>
    """)
    if data:
        color=toggle(color)
        st.session_state["stock"][id]=color
