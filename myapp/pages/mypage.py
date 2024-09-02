import os
import sys
import json

from bson import ObjectId
import streamlit as st
from streamlit_calendar import calendar
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/mount/src/nippo/myapp/utils/')))
from data_fetch import get_client, init_database, fetch_async,get_user_info
from models import Event

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/mount/src/nippo/myapp/frontend/')))
from component_list import hide_sidebar, hide_side_button




def parse2fullcal(events):
    fullcalendar_events = []
    for event in events:
        fullcalendar_event = {
            "id": str(event.id),
            "title": event.customer,
            "start": event.start_time.isoformat(),
            "end": event.end_time.isoformat(),
            "extendedProps": {
                "address": event.address,
                "purpose": event.purpose
            }
        }
        fullcalendar_events.append(fullcalendar_event)
    return fullcalendar_events

async def main():

    user_id = st.session_state.get("success_id")
    user_info=get_user_info(user_id)
    username = str(user_info["user_name"])
    name = str(user_info["Name"])
    bookmarks=user_info["bookmark"]
    
    if username == "None":
        st.switch_page("pages/login.py")

    st.title(name+"のマイページ")
    
    # if st.button("自分の書いた日報を見る"):
    #     st.switch_page("pages/seemynippo.py")
    
    # if st.button("他の人が書いた日報を見る"):
    # # クエリパラメータを設定して、search.pyページに遷移
    #     st.switch_page("pages/search_nippo.py")

    
    client = get_client()
    filter={"user_id": user_id}
    try:
        events_list = await fetch_async(filter,model=Event)
    except:
        await init_database(client,models=[Event])
        events_list = await fetch_async(filter,model=Event)
    filter_bookmarks={"_id":{ "$in": bookmarks}}
    try:
        bookmark_info= await fetch_async(filter_bookmarks)
    except:
        await init_database(client)
        bookmark_info= await fetch_async(filter_bookmarks)
        
        
    # st.markdown(
    #     f"""
    #     <p class="h2 text-center">
    #     <hr>

    #     <div class="card-body">
    #         <p class="h5">ユーザネーム:{username}</p>
    #         <p class="h5">名前　：{name}</p>
    #     </div>
    #     <hr>
    #     """
    #     ,unsafe_allow_html=True)
    
    st.write("お疲れ様です、"+username+"さん。日報管理システムへようこそ!")
    calendar_events = parse2fullcal(events_list)
    calendar_options = {
        "minTime":'08:00:00',
        "maxTime": '18:00:00', 
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "list,dayGridWeek,dayGridMonth",
        },
    }

    if st.button("イベントを新しく登録"):
        st.switch_page("pages/make_event.py")

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


    # 初期状態の設定
    if 'show_modal' not in st.session_state:
        st.session_state['show_modal'] = False

    # eventClick コールバックの処理
    if cal.get("eventClick"):
        event_data = cal["eventClick"]["event"]
        st.session_state['show_modal'] = True
        st.session_state['event_data'] = event_data  # イベントデータを保存
        st.switch_page("pages/Event.py")
    
    # Define the header outside of the scrollable div
    st.markdown("<h2>ブックマークした投稿</h2>", unsafe_allow_html=True)

    # Define the scrollable list with improved styling
    list_html = ""
    for info in bookmark_info:
        nippo_customer = info.customer
        nippo_purpose = info.purpose
        nippo_contents = info.contents
        list_html += f"<div class='list-group-item' style='border: 1px solid #ddd; margin-bottom: 10px; padding: 10px; border-radius: 5px;'><strong>{nippo_customer} - {nippo_purpose}</strong><br><span>{nippo_contents}</span></div>"

    # Render the scrollable div
    st.markdown(
        f"<div class='scrollable-list' style='height: 300px; overflow-y: scroll; padding-right: 10px; border: 1px solid #ccc; border-radius: 5px;'>{list_html}</div>",
        unsafe_allow_html=True
    )


a = "createbyhands"
hide_side_button()

asyncio.run(main())



