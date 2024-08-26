import streamlit as st

# タイトル
st.title('日報管理システムにログインする')

st.write("現在はID=abc ,パスワード=123456のみ対応しています")
# ログインIDの入力ボックス
login_id = st.text_input('ログインID:')

# パスワードの入力ボックス
password = st.text_input('パスワード:', type='password')

# ログインボタン
if st.button('ログイン'):
    # ログイン処理の部分（例: IDとパスワードのチェックなど）
    if login_id == "abc" and password == "123456": 
        #実際にはdb内にあるかを判定する
        st.success("ログイン成功!")
        st.switch_page("pages/toppage.py")
    else:
        st.error("ログインIDまたはパスワードが間違っています。")
