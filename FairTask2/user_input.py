import streamlit as st
import json
import os
from datetime import date

USERS_FILE = "data/users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def run():
    st.header("👥 メンバー登録")

    name = st.text_input("名前")
    unavailable = st.date_input("不在日（任意）", [], format="YYYY-MM-DD")

    if st.button("登録"):
        users = load_users()
        users.append({
            "name": name,
            "points": 0,
            "unavailable": [str(unavailable)] if isinstance(unavailable, date) else [str(d) for d in unavailable]
        })
        save_users(users)
        st.success(f"{name} を登録したよ！")
        st.rerun()

    st.subheader("📋 メンバー一覧")
    users = load_users()
    for i, user in enumerate(users):
        col1, col2, col3 = st.columns([3, 3, 1])
        col1.write(f"🧍‍♂️ {user['name']}（ポイント：{user['points']}）")
        col2.write(f"不在日: {', '.join(user['unavailable']) or 'なし'}")
        if col3.button("🗑️ 削除", key=f"del-user-{i}"):
            users.pop(i)
            save_users(users)
            st.success(f"{user['name']} を削除したよ！")
            st.rerun()
