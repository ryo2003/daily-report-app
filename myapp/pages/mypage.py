
import streamlit as st
from streamlit_calendar import calendar
import json

calendar_options = {
    "selectable": True,
}

calendar_events = [
    {
        "title": "Event 1",
        "start": "2024-08-26T08:30:00",
        "end": "2024-08-26T10:30:00",
        "resourceId": "a",
    },
    {
        "title": "Event 2",
        "start": "2024-08-26T07:30:00",
        "end": "2024-08-26T10:30:00",
        "resourceId": "b",
    },
    {
        "title": "Event 3",
        "start": "2024-08-26T10:40:00",
        "end": "2024-08-26T12:30:00",
        "resourceId": "a",
    }
]

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
if calendar.get("eventClick"):
    event_data = calendar["eventClick"]["event"]
    st.dialog(f"イベントがクリックされました: {event_data['title']} 開始時間: {event_data['start']}")
    st.write(f"イベントがクリックされました: {event_data['title']} 開始時間: {event_data['start']}")
