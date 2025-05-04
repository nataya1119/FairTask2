# fairtask_v2/app.py
import streamlit as st
import assign_view
import user_input
import task_input
import history_view
import thanks_ranking
import task_swap_view

st.set_page_config(page_title="FairTaskにゃ", layout="centered")

st.sidebar.title("🐾 メニュー")
page = st.sidebar.radio("にゃにする？", (
    "割り当て管理",
    "ユーザー登録",
    "タスク登録",
    "完了率ランキング",
    "Thanksランキング",
    "タスク交代依頼"
))

if page == "割り当て管理":
    assign_view.run()
elif page == "ユーザー登録":
    user_input.run()
elif page == "タスク登録":
    task_input.run()
elif page == "完了率ランキング":
    history_view.run()
elif page == "Thanksランキング":
    thanks_ranking.run()
elif page == "タスク交代依頼":
    task_swap_view.run()
