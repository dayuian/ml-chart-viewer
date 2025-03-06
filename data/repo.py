import sqlite3
import os
import pandas as pd

db_file = "data/files.db"
os.makedirs("data", exist_ok=True)  # 確保 `data/` 目錄存在

def get_db_connection():
    """取得 SQLite 連線"""
    return sqlite3.connect(db_file, check_same_thread=False)

def init_db():
    """初始化 SQLite 檔案管理表"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT UNIQUE,
                filetype TEXT,
                filesize INTEGER,
                filepath TEXT,
                upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def save_file_info(file_info):
    """儲存檔案資訊至資料庫"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO files (filename, filetype, filesize, filepath, upload_time)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (file_info["filename"], file_info["filetype"], file_info["filesize"], file_info["filepath"]))
            conn.commit()
        except sqlite3.IntegrityError:
            print(f"⚠️ 檔案 `{file_info['filename']}` 已存在，略過寫入。")

def get_all_files():
    """取得所有檔案記錄"""
    with get_db_connection() as conn:
        try:
            return pd.read_sql("SELECT id, filename, filetype, filesize, upload_time FROM files", conn)
        except Exception as e:
            print(f"⚠️ 無法讀取資料庫: {e}")
            return pd.DataFrame()

def delete_files(file_ids):
    """批次刪除 SQLite 記錄"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        for file_id in file_ids:
            cursor.execute("SELECT filepath FROM files WHERE id=?", (file_id,))
            file = cursor.fetchone()
            if file and os.path.exists(file[0]):
                os.remove(file[0])  # 刪除實際檔案
            cursor.execute("DELETE FROM files WHERE id=?", (file_id,))
        conn.commit()

def get_file_by_id(file_id):
    """根據 ID 取得檔案路徑"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT filepath FROM files WHERE id=?", (file_id,))
        file = cursor.fetchone()
        return file[0] if file else None

def get_latest_file():
    """取得最新上傳的檔案"""
    df_files = get_all_files()
    if df_files.empty:
        return pd.DataFrame()
    
    latest_file_id = df_files["id"].iloc[-1]
    file_path = get_file_by_id(latest_file_id)
    
    if file_path is None or not os.path.exists(file_path):
        print("⚠️ 找不到最新檔案")
        return pd.DataFrame()
    
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"⚠️ 無法讀取 CSV 檔案: {e}")
        return pd.DataFrame()

# ✅ 初始化資料庫
init_db()
