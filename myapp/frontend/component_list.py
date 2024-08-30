import streamlit as st
from st_bridge import bridge, html
import random

#汎化関数
def icon_emb(icon_id: str) ->str:
    return f"<i class='bi bi-{icon_id}'></i></label>"

def icon_toggle(icon_id: str,nippo_id : str,classes: list = [], click_output="clicked",color="btn-outline-secondary") -> str:
    classes = " ".join(classes)
    rnum=int(random.random()*1000)
    html_output = f"""
        <input type="checkbox" class="btn-check" id="btn-check-{rnum}-outlined" autocomplete="off">
        <label class="btn {color} {classes}" for="btn-check-{rnum}-outlined" onClick="stBridges.send('{icon_id}_{nippo_id}', '{click_output}')">
        <i class="bi bi-{icon_id}"></i></label><br>
    """
    return html_output

def nippo_card(username,purpose,customer,src_time):
    

#個別の関数
