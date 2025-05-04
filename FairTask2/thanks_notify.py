# fairtask_v2/thanks_notify.py
import json
import os
from datetime import datetime
from discord_notify import send_notification

DATA_DIR = "data/"
THANKS_LOG = os.path.join(DATA_DIR, "thanks_log.json")


def load_thanks():
    if not os.path.exists(THANKS_LOG):
        return []
    with open(THANKS_LOG, "r", encoding="utf-8") as f:
        return json.load(f)


def save_thanks(log):
    with open(THANKS_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)


def record_thanks(giver, receiver, task, date):
    log = load_thanks()
    new_entry = {
        "from": giver,
        "to": receiver,
        "task": task,
        "date": date,
        "timestamp": datetime.now().isoformat()
    }
    log.append(new_entry)
    save_thanks(log)

    # Discord通知
    message = f"💌 {giver}さんが {receiver}さんに「{task}」のお仕事で Thanks を送ったにゃ！\n\nありがとにゃ〜〜🐾"
    send_notification(message)
