
import streamlit as st
from streamlit_calendar import calendar
import json
calendar_options = {
    "selectable": True,
}

with open('demo_data.json', 'r') as f:
    calendar_events = json.load(f)

json_open = open("demo_data.json", 'r')
calendar_events = json.load(json_open)
custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
"""

calendar = calendar(events=calendar_events, options=custom_css, custom_css=custom_css, callbacks=['dateClick', 'eventClick', 'eventChange', 'eventsSet', 'select'], license_key='CC-Attribution-NonCommercial-NoDerivatives', key=None)

# 初期状態の設定
if 'show_modal' not in st.session_state:
    st.session_state['show_modal'] = False

# eventClick コールバックの処理
if calendar.get("eventClick"):
    event_data = calendar["eventClick"]["event"]
    st.session_state['show_modal'] = True
    st.session_state['event_data'] = event_data  # イベントデータを保存

# ダイアログの表示制御
if st.session_state.get('show_modal'):
    event_data = st.session_state['event_data']
    st.write("### イベント詳細")
    st.write(f"タイトル: {event_data['title']}")
    st.write(f"開始時間: {event_data['start']}")
    st.write(f"終了時間: {event_data['end']}")

    option = st.radio(
        "日報の作成方法を選んでください:",
        ('手動で作成', '対話で作成'))

# ボタンがクリックされた時の処理
    if st.button("日報を作成"):
        if option == '手動で作成':
            st.switch_page("pages/createbyhands.py")
        elif option == '対話で作成':
            st.switch_page("pages/chatpage.py")
    # 閉じるボタン
    if st.button("閉じる"):
        st.session_state['show_modal'] = False  # モーダルを閉じる

