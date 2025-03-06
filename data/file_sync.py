import os
from data.repo import get_all_files, save_file_info, delete_files

def sync_files_with_database():
    """同步 `data/` 目錄與 SQLite，確保紀錄正確"""
    data_folder = "data"
    os.makedirs(data_folder, exist_ok=True)

    # 取得資料庫中的檔案列表
    df_files = get_all_files()
    db_files = set(df_files["filename"].tolist()) if not df_files.empty else set()

    # 取得實際 `data/` 內的檔案列表
    actual_files = set(os.listdir(data_folder))

    # ✅ 找出 `data/` 內有，但 SQLite 沒有記錄的檔案
    missing_in_db = actual_files - db_files
    for filename in missing_in_db:
        file_path = os.path.join(data_folder, filename)
        file_info = {
            "filename": filename,
            "filetype": "csv",
            "filesize": os.path.getsize(file_path),
            "filepath": file_path,
        }
        save_file_info(file_info)
        print(f"✅ 修正: `{filename}` 已自動加入 SQLite")

    # ❌ 找出 SQLite 有記錄，但 `data/` 內已刪除的檔案
    missing_in_folder = db_files - actual_files
    if missing_in_folder:
        file_ids = df_files[df_files["filename"].isin(missing_in_folder)]["id"].tolist()
        delete_files(file_ids)
        print(f"🗑 修正: `{len(file_ids)}` 筆資料已從 SQLite 移除 (檔案不存在)")
