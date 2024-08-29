import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/app/utils/')))
from login_utils import login



# CSSでスタイルを追加
st.markdown("""
    <style>
    .main-title {
        font-size: 40px;
        color: #4a7a8c;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .input-box {
        width: 300px;
        margin: auto;
        margin-bottom: 20px;
    }
    .stTextInput > div > input {
        padding: 10px;
        font-size: 16px;
        border: 1px solid #ddd;
        border-radius: 5px;
    }
    .login-button {
        width: 100%;
        padding: 10px;
        font-size: 18px;
        background-color: #4a7a8c;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .login-button:hover {
        background-color: #366b77;
    }
    </style>
""", unsafe_allow_html=True)

# タイトル
st.markdown('<h1 class="main-title">日報管理システムにログインする</h1>', unsafe_allow_html=True)

# ログインIDの入力ボックス
login_id = st.text_input("ユーザ名:", key="login_id", placeholder="ユーザ名を入力", label_visibility="collapsed")

# パスワードの入力ボックス
password = st.text_input('パスワード:', type='password', key="password", placeholder="パスワードを入力", label_visibility="collapsed")

# ログインボタン
if st.button('ログイン',key="login_button"):
    # ログイン処理の部分（例: IDとパスワードのチェックなど)
    login(login_id,password)
