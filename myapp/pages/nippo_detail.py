import os
import sys

from bson import ObjectId
import streamlit as st
import asyncio
from st_bridge import bridge, html

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/frontend/')))
from data_fetch import  init_database, fetch_async, get_username,get_client
from component_list import icon_toggle,icon_emb
async def main():
    # ログインしているユーザのid取得
    user_id = st.session_state.get("success_id")
    # 閲覧している日報のid取得(仮)
    nippo_id = st.session_state.get('selected_nippo_id', "66cfe05b8d90b8e8fead968b")

    
    filter = {
        "_id":nippo_id
    }
    # nippo_idからnippoデータを取得
    client = get_client()
    await init_database(client)
    nippo = await fetch_async(filter)
    # nippo_idの日報の作成者をユーザID取得
    print(nippo)
    author_id = nippo[0].user_id
    customer=nippo[0].customer
    event_time = nippo[0].event_time
    timestamp = nippo[0].timestamp
    author_username = get_username(author_id)
    
    # nippo_idからeventidを取得して、イベント名を取得するコードを書く必要あり
    # 現在は仮のイベント名を入力
    event_name = "A会社との商談"
    bridge_name=f"{user_id}_{nippo_id}"
    data = bridge(f"{user_id}_{nippo_id}", default="")

    contents = nippo[0].contents
    st.markdown(f"""
                <p class="h1">{event_name}の日報</p>
        <div class="d-flex justify-content-between align-items-center">
        <div>
            <div class="d-flex">
            <i class="bi bi-person-circle mx-1"></i>
                <div class="mx-1">{author_username}</div>
            </div>
            <div class="d-flex">
            <i class="bi bi-building mx-1"></i>
                <div class="mx-1">{customer}</div>
            </div>
        </div>
</div>
""",unsafe_allow_html=True)
    html(f"""
                <div class="d-flex justify-content-between align-items-center">
    <div class="d-flex">
        <i class="bi bi-calendar mx-1 align-self-center"></i>
        <div>
            <div class="small mx-1">イベント時間：{event_time.strftime("%Y-%m-%d %H:%M:%S")}</div>
            <div class="small mx-1">日報作成日：{timestamp.strftime("%Y-%m-%d %H:%M:%S")}</div>
        </div>
    </div>
    <div class="d-flex">
    <div>
        <input type="checkbox" class="btn-check" id="btn-check-1-outlined" autocomplete="off" {"checked" if st.session_state.get(f"iine_{nippo_id}_{user_id}") == "clicked" else ""}>
        <label class="btn btn-outline-primary mx-1" for="btn-check-1-outlined" onClick="stBridges.send('{bridge_name}', 'iine')">
        <i class="bi bi-hand-thumbs-up-fill"></i></label><br>
    </div>

    <div>
        <input type="checkbox" class="btn-check" id="btn-check-2-outlined" autocomplete="off" {"checked" if st.session_state.get(f"stock_{nippo_id}_{user_id}") == "clicked" else ""}>
        <label class="btn btn-outline-secondary mx-1" for="btn-check-2-outlined" onClick="stBridges.send('{bridge_name}', 'stock')">
        <i class="bi bi-bookmark"></i></label><br>
    </div>
</div>
""")
   
    st.markdown("<hr>",unsafe_allow_html=True)
    st.write(contents)
    # カスタム評価ウィジェットの呼び出し
    if data=="iine":
        st.write(data)
        if st.session_state.get(f"iine_{nippo_id}_{user_id}") == "clicked":
            i_flag="unclicked"
            st.session_state[f"iine_{nippo_id}_{user_id}"]=i_flag
        else:
            i_flag="clicked"
            st.session_state[f"iine_{nippo_id}_{user_id}"]=i_flag
            print(f"{user_id}にいいねが押されました")
        st.write("iine",i_flag)            
        
    elif data=="stock":
        if st.session_state.get(f"stock_{nippo_id}_{user_id}") == "clicked":
            s_flag = "unclicked"
            st.session_state[f"stock_{nippo_id}_{user_id}"]=s_flag
        else:     
            s_flag="clicked"
            st.session_state[f"stock_{nippo_id}_{user_id}"]=s_flag
            print(f"{user_id}にstockが押されました")
        st.write("stock",s_flag)
        
        
asyncio.run(main())