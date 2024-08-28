import streamlit as st
from bson import ObjectId
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))
from data_fetch import getnippo_from_nippoid

#ログインしているユーザのid取得
userid = st.session_state.get("success_id")

#閲覧している日報のid取得(仮)
nippo_id = ObjectId("66ced4e408302a8a9e19a132")

nippo = getnippo_from_nippoid(nippo_id)
st.write(nippo["contents"])

