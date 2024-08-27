import streamlit as st


if st.session_state.get('event_data'):
    event_data = st.session_state['event_data']
    title = event_data['title']
    st.title(f"イベント:{title}")
    st.write("### イベント詳細")
    st.write(f"開始時間: {event_data['start']}")
    st.write(f"終了時間: {event_data['end']}")
    # ダイアログの表示制御

    if st.button("ページ遷移"):
        st.switch_page("pages/chatpage.py")

else:
    title= "NonDATA"

