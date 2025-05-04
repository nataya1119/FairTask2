# fairtask_v2/task_swap_view.py
import streamlit as st
import json
import os
from datetime import datetime
from discord_notify import send_notification

DATA_DIR = "data/"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
SWAPS_FILE = os.path.join(DATA_DIR, "swap_requests.json")

def get_assignment_file(date_str):
    month = date_str[:7]  # 'YYYY-MM'
    return os.path.join(DATA_DIR, f"assignments_{month}.json")

def load_json(file):
    if not os.path.exists(file):
        return {} if file == SWAPS_FILE else []
    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_task_assignments(date_str, username):
    file = get_assignment_file(date_str)
    assignments = load_json(file)
    today = assignments.get(date_str, [])
    return [task for task in today if task["assigned_to"] == username and not task.get("done", False)]

def run():
    st.header("🔄 タスク交代依頼")
    
    date_str = st.date_input("対象日を選んでにゃ〜").strftime("%Y-%m-%d")
    users = load_json(USERS_FILE)
    swap_requests = load_json(SWAPS_FILE)
    
    current_user = st.selectbox("だれが操作してるにゃ？", [u["name"] for u in users])
    
    st.subheader("新しい交代依頼を作るにゃ")
    
    # 自分のタスクを選択
    my_tasks = get_task_assignments(date_str, current_user)
    if not my_tasks:
        st.info("今日はもう完了済みか、タスクが割り当てられてないにゃ！🐱")
    else:
        task_options = [task["task"] for task in my_tasks]
        selected_task = st.selectbox("交代してほしいタスクを選ぶにゃ", task_options)
        
        # 交代相手を選択
        other_users = [u["name"] for u in users if u["name"] != current_user]
        selected_user = st.selectbox("交代してほしい相手を選ぶにゃ", other_users)
        
        reason = st.text_area("理由を教えるにゃ（任意）", placeholder="今日は遅くなりそうなんだ...")
        
        if st.button("交代依頼を出すにゃ！"):
            request_id = f"{date_str}_{current_user}_{selected_task}_{datetime.now().strftime('%H%M%S')}"
            
            # 新しい交代依頼を作成
            new_request = {
                "id": request_id,
                "date": date_str,
                "task": selected_task,
                "from_user": current_user,
                "to_user": selected_user,
                "reason": reason,
                "status": "pending",  # pending, accepted, rejected
                "created_at": datetime.now().isoformat()
            }
            
            if date_str not in swap_requests:
                swap_requests[date_str] = []
            
            swap_requests[date_str].append(new_request)
            save_json(SWAPS_FILE, swap_requests)
            
            # Discord通知
            message = f"🔄 【交代依頼】{current_user}さんから{selected_user}さんへ\n"
            message += f"📅 {date_str}の「{selected_task}」について交代依頼が出たにゃ！\n"
            if reason:
                message += f"💬 理由: {reason}\n"
            message += "\nアプリで確認するにゃ〜"
            send_notification(message)
            
            st.success("交代依頼を送信したにゃ！")
            st.rerun()
    
    # 自分宛ての依頼を表示
    st.subheader("あなた宛ての依頼にゃ")
    pending_requests = []
    
    for date_requests in swap_requests.values():
        for req in date_requests:
            if req["to_user"] == current_user and req["status"] == "pending":
                pending_requests.append(req)
    
    if not pending_requests:
        st.info("あなた宛ての依頼はないにゃ！")
    else:
        for req in pending_requests:
            st.write(f"🧹 {req['task']} （{req['date']}）")
            st.write(f"👤 依頼者: {req['from_user']}")
            if req["reason"]:
                st.write(f"💬 理由: {req['reason']}")
            
            col1, col2 = st.columns(2)
            if col1.button("承認するにゃ", key=f"accept_{req['id']}"):
                # 依頼を承認
                for date_requests in swap_requests.values():
                    for r in date_requests:
                        if r["id"] == req["id"]:
                            r["status"] = "accepted"
                            r["responded_at"] = datetime.now().isoformat()
                
                # タスクの担当者を交換
                file = get_assignment_file(req["date"])
                assignments = load_json(file)
                today = assignments.get(req["date"], [])
                
                for task in today:
                    if task["task"] == req["task"] and task["assigned_to"] == req["from_user"]:
                        task["assigned_to"] = req["to_user"]
                        task["swapped"] = True
                        task["original_assignee"] = req["from_user"]
                
                save_json(file, assignments)
                save_json(SWAPS_FILE, swap_requests)
                
                # Discord通知
                message = f"✅ 【交代成立】{req['from_user']}さんから{req['to_user']}さんへ\n"
                message += f"📅 {req['date']}の「{req['task']}」の交代が成立したにゃ！\n"
                message += f"ありがとにゃ〜🐱"
                send_notification(message)
                
                st.success("交代を承認したにゃ！")
                st.rerun()
            
            if col2.button("断るにゃ", key=f"reject_{req['id']}"):
                # 依頼を拒否
                for date_requests in swap_requests.values():
                    for r in date_requests:
                        if r["id"] == req["id"]:
                            r["status"] = "rejected"
                            r["responded_at"] = datetime.now().isoformat()
                
                save_json(SWAPS_FILE, swap_requests)
                
                # Discord通知
                message = f"❌ 【交代拒否】{req['from_user']}さんから{req['to_user']}さんへの\n"
                message += f"📅 {req['date']}の「{req['task']}」交代依頼は拒否されたにゃ..."
                send_notification(message)
                
                st.error("交代を断ったにゃ")
                st.rerun()
    
    # 履歴表示
    st.subheader("交代依頼の履歴にゃ")
    
    my_history = []
    for date_requests in swap_requests.values():
        for req in date_requests:
            if req["from_user"] == current_user or req["to_user"] == current_user:
                if req["status"] != "pending":  # 未対応のものは上で表示済み
                    my_history.append(req)
    
    if not my_history:
        st.info("まだ履歴はないにゃ")
    else:
        for req in sorted(my_history, key=lambda x: x.get("responded_at", ""), reverse=True)[:5]:  # 最新5件
            status_emoji = "✅" if req["status"] == "accepted" else "❌"
            st.write(f"{status_emoji} {req['date']}の「{req['task']}」")
            st.write(f"👤 {req['from_user']} → {req['to_user']}")
            st.write("---")
