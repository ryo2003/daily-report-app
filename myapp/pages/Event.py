import sys
import os
import streamlit as st
from streamlit_calendar import calendar
from st_bridge import bridge, html

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))

from data_register import insert_chat

if st.session_state.get('event_data'):
    event_data = st.session_state['event_data']
    id = event_data['id']
    title = event_data['title']
    start_time = event_data['start']
    end_time = event_data['end']
    adress = event_data["extendedProps"]["address"]
    # st.map(location.latitude,location.longitude)
    # event_id = event_data["event_id"]
    st.title(f"イベント:{title}")
    st.write("### イベント詳細")
    st.write(f"開始時間: {start_time}")
    st.write(f"終了時間: {end_time}")
    calendar_options = {
        "initialView": 'timelineDay',
        "initialDate":start_time,
        "height": 200,
        "minTime":'08:00:00',
        "maxTime": '18:00:00', 

    }
    calendar_events=[{
        "id": str(id),
        "title":title,
        "start": start_time,
        "end": end_time,
    }]
    custom_css="""
        .fc-event-past {
            opacity: 0.8;
            border-radius: 5%;
            height:50px;
            margin: 25px 0px;
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
    cal = calendar(events=calendar_events, options=calendar_options,custom_css=custom_css, callbacks=['dateClick', 'eventClick', 'eventChange', 'eventsSet', 'select'], license_key='CC-Attribution-NonCommercial-NoDerivatives', key=None)
    st.write(f"場所: {adress}")
    st.markdown(f"""
                <iframe
src="https://www.google.com/maps?
output=embed&z=15&ll=35.6812405,139.7649308&q={adress}"
width="100%"
height="500px"
frameborder="0"
style="border: 0;"
allowfullscreen=""
aria-hidden="false"
tabindex="0"
/>
""",unsafe_allow_html=True)
    
    # ダイアログの表示制御
    toggle = bridge(f"toggle", default="")
    html(f"""
         <input type="radio" class="btn-check" name="options-outlined" id="success-outlined" autocomplete="off" checked>
<label class="btn btn-outline-success" for="success-outlined" onClick="stBridges.send('toggle', 'syudo')">手動で作成</label>

<input type="radio" class="btn-check" name="options-outlined" id="danger-outlined" autocomplete="off">
<label class="btn btn-outline-success" for="danger-outlined" onClick="stBridges.send('toggle', 'taiwa')">自動で作成</label>
         """)
    if st.button("日報を作成"):
        if toggle == 'syudo':
            st.switch_page("pages/createbyhands.py")
        elif toggle == 'taiwa':
            # insert_chat()
            st.switch_page("pages/chatpage.py")

else:
    title= "NonDATA"

