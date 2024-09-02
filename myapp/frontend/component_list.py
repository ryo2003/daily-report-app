import streamlit as st
from st_bridge import bridge, html
import random

#汎化関数
def icon_emb(icon_id: str) ->str:
    return f"<i class='bi bi-{icon_id}'></i></label>"

def icon_toggle(icon_id: str,nippo_id : str,bridge_name: str=None,classes: list = [], click_output="clicked",color="btn-outline-secondary",bridge_key=None,) -> str:
    classes = " ".join(classes)
    rnum=int(random.random()*1000)
    if bridge_key:
        html_output = f"""
            <input type="checkbox" class="btn-check" id="btn-check-{rnum}-outlined" autocomplete="off">
            <label class="btn {color} {classes}" for="btn-check-{rnum}-outlined" >
            <i class="bi bi-{icon_id}"></i></label><br>
        """
    else:
        html_output = f"""
        <input type="checkbox" class="btn-check" id="btn-check-{rnum}-outlined" autocomplete="off">
        <label class="btn {color} {classes}" for="btn-check-{rnum}-outlined" onClick="stBridges.send('{bridge_name}', '{click_output}')">
        <i class="bi bi-{icon_id}"></i></label><br>
    """
    return html_output

def nippo_card(username,purpose,customer,src_time,nippo_id,contents):
    # Define HTML with JavaScript to handle button clicks
    html_tem=f"""
<div>
    <div class="card">
        <div class="card-body">
            <h5 class="card-title py-0">{customer}-{purpose}</h5>
            <hr>
            <div class="d-flex d-flex justify-content-between align-items-center">
                <p class="card-text"><i class="bi bi-person-circle mx-1"></i> {username}</p>
                <p class="card-text small p-0 text-end">{src_time}</p>
            </div>
            <p class="card-text"><i class="bi bi-building mx-1"></i> {customer}</p>
            <p class="card-text text-truncate">{contents}</p>

        <div class="d-flex justify-content-between align-items-center">
            <div>
                カテゴリー：<div href="#" class="btn btn-primary" class="text-light">
                    {purpose}
                </div>
            </div>
            <div class="d-flex justify-content-between">
                {icon_toggle("hand-thumbs-up-fill",nippo_id,"bridge_name",classes=["mx-1"],click_output="clicked",color="btn-outline-primary",bridge_key=f"bridge-key_i_{nippo_id}")}
                {icon_toggle("bookmark",nippo_id,"bridge_name",classes=["mx-1"],click_output="clicked",bridge_key=f"bridge-key_b_{nippo_id}")}
                <div class="btn btn-outline-primary text-end" onClick="stBridges.send('nippo-bridge-{nippo_id}', 'Nippo ID: {nippo_id}')">
                <i class="bi bi-box-arrow-up-right"></i>
                </div>
            </div>

        </div>
        </div>
    </div>
</div>
    """
    return html_tem
#個別の関数
