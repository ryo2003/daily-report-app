import streamlit as st
import pandas as pd

# 仮の日報データ
# データベースができたらそっちから引っ張る
data = {
    "報告者": ["山田太郎", "佐藤花子", "鈴木一郎"],
    "企業名": ["株式会社A", "株式会社B", "株式会社C"],
    "訪問時間": ["2024-08-20 10:00", "2024-08-21 14:00", "2024-08-22 09:00"],
    "訪問目的": ["提案", "フォロー", "クローズ"],
    "お客様の課題": ["価格競争が激しい", "納期の短縮", "競合他社が強力"],
}

# データフレームに変換
df = pd.DataFrame(data)

st.title("日報検索")

# 検索フォーム
st.sidebar.header("検索条件")
selected_name = st.sidebar.selectbox("報告者を選択してください", options=["すべて"] + list(df["報告者"].unique()))
selected_company = st.sidebar.selectbox("企業名を選択してください", options=["すべて"] + list(df["企業名"].unique()))
selected_purpose = st.sidebar.selectbox("訪問目的を選択してください", options=["すべて"] + list(df["訪問目的"].unique()))

# 検索ボタン
search_button = st.sidebar.button("検索")

#selected_name/company/purposeをutilsの検索functionに入れる
if search_button :
    st.write("報告者："+selected_name+" 企業名："+selected_company+" 訪問目的:"+selected_purpose+"　での検索結果は以下です")
    st.write("まだ検索用の関数が作られていないためエラーがでます")
    search_result = utils.search(selected_name,selected_company,selected_purpose)
    st.write(search_result)
