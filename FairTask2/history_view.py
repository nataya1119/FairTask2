# fairtask_v2/history_view.py
import streamlit as st
import json
import os
from collections import defaultdict

DATA_DIR = "data/"
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
ASSIGN_FILE = os.path.join(DATA_DIR, "assignments.json")


def load_json(file):
    if not os.path.exists(file):
        return []
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def run():
    st.header("📊 完了率ランキングにゃ！")

    history = load_json(HISTORY_FILE)
    assignments = {}
    for fname in os.listdir(DATA_DIR):
        if fname.startswith("assignments_") and fname.endswith(".json"):
            file_data = load_json(os.path.join(DATA_DIR, fname))
            if isinstance(file_data, dict):
                assignments.update(file_data)

    assigned_counts = defaultdict(int)
    completed_counts = defaultdict(int)
    swapped_counts = defaultdict(int)  # 交代受け入れ回数を追跡

    # 履歴から交代受け入れ回数をカウント
    for item in history:
        if item.get("swapped") and item["name"] != item.get("original_assignee"):
            swapped_counts[item["name"]] += 1

    # 割り当て数と完了数をカウント
    for date_str, entries in assignments.items():
        for entry in entries:
            name = entry["assigned_to"]
            if name != "未割り当て":
                assigned_counts[name] += 1
                if entry.get("done"):
                    completed_counts[name] += 1

    all_names = set(assigned_counts.keys()).union(completed_counts.keys())

    st.write("### 🐾 みんなの完了率")
    data = []
    
    for name in sorted(all_names):
        total = assigned_counts.get(name, 0)
        done = completed_counts.get(name, 0)
        rate = f"{(done / total * 100):.1f}%" if total > 0 else "-"
        swaps = swapped_counts.get(name, 0)
        data.append((name, total, done, rate, swaps))

    data.sort(key=lambda x: float(x[3][:-1]) if x[3] != "-" else 0, reverse=True)

    st.table(
        [
            {"名前": name, "割り当て数": total, "完了数": done, "完了率": rate, "交代引受数": swaps}
            for name, total, done, rate, swaps in data
        ]
    )