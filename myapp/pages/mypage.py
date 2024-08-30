import os
import sys
import json

from bson import ObjectId
import streamlit as st
from streamlit_calendar import calendar
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))
from data_fetch import get_client, init_database, fetch_async
from models import Event

def parse2fullcal(events):
    fullcalendar_events = []
    for event in events:
        fullcalendar_event = {
            "id": str(event.id),
            "title": event.customer,
            "start": event.start_time.isoformat(),
            "end": event.end_time.isoformat(),
            "extendedProps": {
                "address": event.address
            }
        }
        fullcalendar_events.append(fullcalendar_event)
    return fullcalendar_events

async def main():
    user_id=ObjectId("66cd29b9157702dc731b0fdd")
    client = get_client()
    filter={"user_id": user_id}
    await init_database(client,models=[Event])
    events_list = await fetch_async(filter,model=Event)
    calendar_events = parse2fullcal(events_list)
    print("aaakfherogiah",calendar_events)
    calendar_options = {
        "minTime":'08:00:00',
        "maxTime": '18:00:00', 
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "list,timelineWeek,dayGridMonth",
        },
    }
    json_open = open("demo_data.json", 'r')
    calendar_events_b = json.load(json_open)
    print(calendar_events,calendar_events_b)
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

    cal = calendar(events=calendar_events, options=calendar_options, custom_css=custom_css, callbacks=['dateClick', 'eventClick', 'eventChange', 'eventsSet', 'select'], license_key='CC-Attribution-NonCommercial-NoDerivatives', key=None)

    if st.session_state.get("success_id"):
        st.write("abc")

    # 初期状態の設定
    if 'show_modal' not in st.session_state:
        st.session_state['show_modal'] = False

    # eventClick コールバックの処理
    if cal.get("eventClick"):
        event_data = cal["eventClick"]["event"]
        st.session_state['show_modal'] = True
        st.session_state['event_data'] = event_data  # イベントデータを保存
        st.switch_page("pages/Event.py")

    # ダイアログの表示制御
    if st.session_state.get('show_modal'):
        event_data = st.session_state['event_data']
        st.write("### イベント詳細")
        st.write(f"タイトル: {event_data['title']}")
        st.write(f"開始時間: {event_data['start']}")
        st.write(f"終了時間: {event_data['end']}")


asyncio.run(main())