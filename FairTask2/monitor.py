'''# fairtask_v2/monitor.py
import json
import os
from datetime import datetime
from collections import defaultdict
from discord_notify import send_notification

DATA_DIR = "data/"
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
ASSIGN_FILE = os.path.join(DATA_DIR, "assignments.json")
THRESHOLD = 0.5  # 50%


def load_json(file):
    if not os.path.exists(file):
        return []
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def monitor():
    now = datetime.now()
    last_month = now.month - 1 if now.month > 1 else 12
    year = now.year if now.month > 1 else now.year - 1
    history = load_json(HISTORY_FILE)
    assignments = load_json(ASSIGN_FILE)

    assigned_counts = defaultdict(int)
    completed_counts = defaultdict(int)

    for date_str, entries in assignments.items():
        date = datetime.strptime(date_str, "%Y-%m-%d")
        if date.month == last_month and date.year == year:
            for entry in entries:
                name = entry["assigned_to"]
                if name != "未割り当て":
                    assigned_counts[name] += 1
                    if entry.get("done"):
                        completed_counts[name] += 1

    low_performers = []

    for name in assigned_counts:
        total = assigned_counts[name]
        done = completed_counts.get(name, 0)
        rate = done / total if total > 0 else 1.0
        if rate < THRESHOLD:
            low_performers.append((name, rate))

    if low_performers:
        message = "⚠️【にゃん注意報】以下のメンバーの完了率が低いにゃ…\n\n"
        for name, rate in low_performers:
            message += f"🐾 {name}: {rate * 100:.1f}%\n"
        message += "\n来月はちょっとだけがんばってほしいにゃ〜！🐱"
        send_notification(message)


if __name__ == "__main__":
    monitor()
'''

# fairtask_v2/monitor.py
import json
import os
from datetime import datetime
from collections import defaultdict
from discord_notify import send_notification

DATA_DIR = "data/"
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")
ASSIGN_FILE = os.path.join(DATA_DIR, "assignments.json")
THRESHOLD = 0.5  # 50%

def load_json(file):
    if not os.path.exists(file):
        return []
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

def monitor():
    now = datetime.now()
    last_month = now.month - 1 if now.month > 1 else 12
    year = now.year if now.month > 1 else now.year - 1
    print(f"📅 対象年月: {year}-{last_month:02d}")

    history = load_json(HISTORY_FILE)
    assignments = load_json(ASSIGN_FILE)

    assigned_counts = defaultdict(int)
    completed_counts = defaultdict(int)

    for date_str, entries in assignments.items():
        date = datetime.strptime(date_str, "%Y-%m-%d")
        if date.month == last_month and date.year == year:
            print(f"🔍 処理中の日付: {date_str}")
            for entry in entries:
                name = entry["assigned_to"]
                if name != "未割り当て":
                    assigned_counts[name] += 1
                    if entry.get("done"):
                        completed_counts[name] += 1

    print(f"📊 割り当て数: {dict(assigned_counts)}")
    print(f"✅ 完了数: {dict(completed_counts)}")

    low_performers = []

    for name in assigned_counts:
        total = assigned_counts[name]
        done = completed_counts.get(name, 0)
        rate = done / total if total > 0 else 1.0
        print(f"🐱 {name} の完了率: {rate:.2f} ({done}/{total})")
        if rate < THRESHOLD:
            low_performers.append((name, rate))

    if low_performers:
        message = "⚠️【にゃん注意報】以下のメンバーの完了率が低いにゃ…\n\n"
        for name, rate in low_performers:
            message += f"🐾 {name}: {rate * 100:.1f}%\n"
        message += "\n来月はちょっとだけがんばってほしいにゃ〜！🐱"
        print("📤 通知送信中にゃ...\n")
        print(message)
        send_notification(message)
    else:
        print("🎉 低完了率のメンバーはいなかったにゃ！")

if __name__ == "__main__":
    monitor()
