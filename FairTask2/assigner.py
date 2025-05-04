# fairtask_v2/assigner.py
import copy

def assign_tasks(date_str, users, tasks, history):
    result = []
    users_copy = copy.deepcopy(users)
    assigned_count = {}  # 各ユーザーの1日割り当て数を追跡にゃ

    for task in sorted(tasks, key=lambda x: -x["points"]):
        available = sorted(
            [u for u in users_copy if date_str not in u["unavailable"]],
            key=lambda x: x["points"]
        )

        # 各ユーザーに対して、すでに2件割り当てられてたら除外にゃ
        available = [u for u in available if assigned_count.get(u["name"], 0) < 2]

        if not available:
            result.append({"task": task["name"], "assigned_to": "未割り当て", "done": False, "thanks": 0, "points": task["points"]})
            continue

        assigned = available[0]  # 最もポイントが少ない人にゃ
        name = assigned["name"]
        assigned_count[name] = assigned_count.get(name, 0) + 1

        result.append({
            "task": task["name"],
            "assigned_to": name,
            "done": False,
            "thanks": 0,
            "points": task["points"]
        })

    return result, users_copy
