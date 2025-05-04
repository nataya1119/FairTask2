import streamlit as st
import json
import os
from assigner import assign_tasks
from discord_notify import send_notification
from thanks_notify import record_thanks

DATA_DIR = "data/"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")


def get_assignment_file(date_str):
    month = date_str[:7]  # 'YYYY-MM'
    return os.path.join(DATA_DIR, f"assignments_{month}.json")

def load_json(file):
    if not os.path.exists(file):
        return {} if file.endswith(".json") else []
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_assignments(date_str):
    file = get_assignment_file(date_str)
    return load_json(file)

def save_assignments(date_str, data):
    file = get_assignment_file(date_str)
    save_json(file, data)

def append_history(entry, date_str):
    history = load_json(HISTORY_FILE)
    history.append({
        "date": date_str,
        "name": entry["assigned_to"],
        "task": entry["task"],
        "points": entry["points"],
        "done_by": entry.get("done_by", entry["assigned_to"])
    })
    save_json(HISTORY_FILE, history)

def run():
    st.header("📅 割り当てと完了管理")

    date_str = st.date_input("対象日を選んでにゃ〜").strftime("%Y-%m-%d")
    users = load_json(USERS_FILE)
    tasks_all = load_json(TASKS_FILE)
    assignments = load_assignments(date_str)
    history = load_json(HISTORY_FILE)

    daily_tasks = tasks_all

    if date_str in assignments:
        st.warning("⚠️ 今日はもう割り当て済みにゃ〜！")
    elif st.button("割り当て開始"):
        result, updated_users = assign_tasks(date_str, users, daily_tasks, history)
        assignments[date_str] = result
        save_assignments(date_str, assignments)
        save_json(USERS_FILE, updated_users)
        st.success("割り当て完了にゃ！")

        message = f"📅 {date_str} のお仕事にゃ〜！\n\n"
        for entry in result:
            message += f"🧹 {entry['task']} → 👤 {entry['assigned_to']}\n"
        send_notification(message)

    st.subheader("📋 今日の担当にゃ〜")
    today = assignments.get(date_str, [])
    updated = False

    current_user = st.selectbox("だれが操作してるにゃ？", [u["name"] for u in users])

    for entry in today:
        col1, col2, col3 = st.columns(3)
        col1.write(f"🧹 {entry['task']}")
        
        # 担当者表示 (交代済みならその表示も)
        if entry.get("swapped"):
            col2.write(f"👤 {entry['assigned_to']} (元: {entry.get('original_assignee')})")
        else:
            col2.write(f"👤 {entry['assigned_to']}")

        if not entry.get("done"):
            if entry["assigned_to"] == current_user:
                if col3.button("完了したにゃ", key=f"{entry['task']}-done"):
                    entry["done"] = True
                    entry["done_by"] = current_user
                    for user in users:
                        if user["name"] == entry["assigned_to"]:
                            user["points"] += entry.get("points", 0)
                            break
                    append_history(entry, date_str)
                    updated = True
            else:
                col3.write("🔒 他の人のタスクにゃ")
        else:
            col3.write("✅ 完了済みにゃ")

        if col3.button("👏", key=f"{entry['task']}-thanks"):
            entry["thanks"] = entry.get("thanks", 0) + 1
            record_thanks(current_user, entry["assigned_to"], entry["task"], date_str)
            updated = True

    if updated:
        save_assignments(date_str, assignments)
        save_json(USERS_FILE, users)