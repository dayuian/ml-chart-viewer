import os

# 資料夾設置
DATA_FOLDER = "data"
DB_FILE = os.path.join(DATA_FOLDER, "files.db")

# 確保 `data/` 資料夾存在
os.makedirs(DATA_FOLDER, exist_ok=True)

# SQLite 設定
SQLITE_CONFIG = {
    "database": DB_FILE,
    "check_same_thread": False,
}

# 預設應用設定
APP_CONFIG = {
    "title": "📊 數據分析與可視化平台",
    "version": "1.0.0",
    "developer": "余彦志 (ian)",
    "contact": "dayuian@hotmail.com",
}