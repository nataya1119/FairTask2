# fairtask_v2/archive_assignments.py
import os
import zipfile
from datetime import datetime, timedelta

DATA_DIR = "data/"
ARCHIVE_DIR = os.path.join(DATA_DIR, "archives")
os.makedirs(ARCHIVE_DIR, exist_ok=True)

# 現在の月より1ヶ月以上前のファイルだけ対象にする
now = datetime.now()
cutoff = now.replace(day=1)  # 今月の1日 → これより前の月が対象

for filename in os.listdir(DATA_DIR):
    if filename.startswith("assignments_") and filename.endswith(".json"):
        try:
            date_part = filename[len("assignments_"):-len(".json")]
            file_month = datetime.strptime(date_part, "%Y-%m")
        except ValueError:
            continue  # フォーマット不一致はスキップ

        if file_month < cutoff:
            json_path = os.path.join(DATA_DIR, filename)
            zip_path = os.path.join(ARCHIVE_DIR, f"{filename[:-5]}.zip")

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(json_path, arcname=filename)

            os.remove(json_path)
            print(f"✅ アーカイブ完了: {filename} → {zip_path}")
