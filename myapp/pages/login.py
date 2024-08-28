import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))
from login_utils import login


# タイトル
st.title('日報管理システムにログインする')

# ログインIDの入力ボックス
login_id = st.text_input('ログインID:')

# パスワードの入力ボックス
password = st.text_input('パスワード:', type='password')



# ログインボタン
if st.button('ログイン'):
    # ログイン処理の部分（例: IDとパスワードのチェックなど)
    login(login_id,password)
