# fairtask_v2/thanks_ranking.py
import json
import os
from collections import defaultdict
import streamlit as st
from datetime import datetime

DATA_DIR = "data/"
THANKS_LOG = os.path.join(DATA_DIR, "thanks_log.json")


def load_thanks():
    if not os.path.exists(THANKS_LOG):
        return []
    with open(THANKS_LOG, "r", encoding="utf-8") as f:
        return json.load(f)


def run():
    st.header("🏅 Thanksランキングにゃ！")

    log = load_thanks()
    if not log:
        st.info("まだ誰にも感謝されてないにゃ…😭")
        return

    # 月フィルター（オプション）
    month = st.selectbox("月を選ぶにゃ", options=sorted({entry['date'][:7] for entry in log}, reverse=True))
    monthly_log = [entry for entry in log if entry['date'].startswith(month)]

    thanks_count = defaultdict(int)
    for entry in monthly_log:
        thanks_count[entry['to']] += 1

    sorted_ranking = sorted(thanks_count.items(), key=lambda x: x[1], reverse=True)

    st.subheader(f"{month} のThanksトップにゃ〜🐾")
    for i, (name, count) in enumerate(sorted_ranking, 1):
        st.write(f"🥇 {i}位: {name}（{count} Thanks）")
