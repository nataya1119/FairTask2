# 🐾 FairTask（フェアタスク）

**FairTask** は、寮生活における共有タスク（掃除、ゴミ出し、片付けなど）を公平に割り当て、完了管理、感謝共有、そして完了率に応じた自動注意喚起まで行う、Streamlit製のネコ型タスク管理アプリです🐱

---

## 🚀 機能一覧

- ✅ タスクの自動割り当て（点数制）
- 📅 過去の完了履歴の可視化
- 💌 Thanksボタンで感謝を記録＆Discord通知
- 🏅 Thanksランキング表示（月別）
- ⚠️ 完了率が50%未満のメンバーをDiscordで注意喚起
- 🔄 タスク交代依頼機能（承認・拒否フロー)
- 📦 月初に過去データを自動ZIPアーカイブ（爆発防止）
- 🌐 サーバー上にホストしてみんなで使える！

---

## 🛠 使用技術

- Python 3.12+
- [Streamlit](https://streamlit.io/)
- JSONファイルベースのデータ管理
- Discord Webhook通知
- GitHub Actions（CI）

---

## 💻 ローカルでの起動方法

```bash
git clone https://github.com/yourname/fairtask.git
cd fairtask
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
