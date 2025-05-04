import streamlit as st
import json
import os

DATA_DIR = "data/"
TASKS_FILE = os.path.join(DATA_DIR, "tasks.json")

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def run():
    st.header("🧼 家事と点数の設定")

    # 🔁 追加入力を先に表示
    st.subheader("タスクの追加")
    name = st.text_input("家事名")
    point = st.number_input("点数", min_value=1, max_value=5, step=1)

    tasks = load_tasks()

    if st.button("追加"):
        if name:
            tasks.append({"name": name, "points": point})
            save_tasks(tasks)
            st.success("追加したにゃ！")
            st.rerun()
        else:
            st.warning("家事名を入力してにゃ")

    # 🔽 一覧は後に表示
    st.write("---")
    for i, task in enumerate(tasks):
        col1, col2, col3 = st.columns([4, 1, 1])
        col1.write(f"{task['name']}")
        col2.write(f"{task['points']}点")
        if col3.button("🗑️", key=f"delete-{i}"):
            tasks.pop(i)
            save_tasks(tasks)
            st.rerun()
