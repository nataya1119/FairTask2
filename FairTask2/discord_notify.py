import os
import requests
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

def send_notification(message):
    if not WEBHOOK_URL:
        print("Discord Webhook URL が設定されていません")
        return
    data = {"content": message}
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code != 204:
            print(f"通知失敗: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"通知中にエラー: {e}")
