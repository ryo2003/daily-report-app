import sys
import os
import streamlit as st

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))

from data_register import insert_chat

if st.session_state.get('event_data'):
    event_data = st.session_state['event_data']
    title = event_data['title']
    start_time = event_data['start']
    end_time = event_data['end']
    adress = event_data["extendedProps"]["address"]
    # event_id = event_data["event_id"]
    st.title(f"イベント:{title}")
    st.write("### イベント詳細")
    st.write(f"開始時間: {start_time}")
    st.write(f"終了時間: {end_time}")
    st.write(f"場所: {adress}")
    
    # ダイアログの表示制御

    option = st.radio(
        "日報の作成方法を選んでください:",
        ('手動で作成', '対話で作成'))

# ボタンがクリックされた時の処理
    if st.button("日報を作成"):
        if option == '手動で作成':
            st.switch_page("pages/createbyhands.py")
        elif option == '対話で作成':
            insert_chat()
            st.switch_page("pages/chatpage.py")
    # 閉じるボタン
    if st.button("閉じる"):
        st.session_state['show_modal'] = False  # モーダルを閉じる

else:
    title= "NonDATA"

