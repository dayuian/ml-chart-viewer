import pandas as pd
import re

def validate_for_sqlite(df):
    """
    檢查數據是否符合 SQLite 匯入條件：
    1. 欄位名稱是否包含空格或特殊字元
    2. 是否有 NaN 欄位
    3. 是否至少有一筆數據
    4. 數據類型是否可存入 SQLite
    """
    errors = []

    # 1️⃣ **檢查欄位名稱**
    invalid_columns = [col for col in df.columns if not re.match(r'^[a-zA-Z0-9_]+$', col)]
    if invalid_columns:
        errors.append(f"❌ 欄位名稱含有不支援的字元: {', '.join(invalid_columns)}")

    # 2️⃣ **檢查 NaN 值**
    if df.isnull().values.any():
        errors.append("❌ 數據包含缺失值，請先清理後再存入 SQLite")

    # 3️⃣ **檢查是否有數據**
    if df.empty:
        errors.append("❌ 數據表為空，無法存入 SQLite")

    # 4️⃣ **檢查數據類型**
    unsupported_types = df.select_dtypes(exclude=["int", "float", "object"]).columns.tolist()
    if unsupported_types:
        errors.append(f"❌ 包含 SQLite 不支援的數據類型: {', '.join(unsupported_types)}")

    return errors

def validate_numeric_columns(df):
    """
    確保數值型欄位只包含數值，避免存入 SQLite 時發生錯誤。
    """
    errors = []
    numeric_columns = df.select_dtypes(include=["int", "float"]).columns

    for col in numeric_columns:
        if not pd.to_numeric(df[col], errors='coerce').notna().all():
            errors.append(f"⚠️ 欄位 `{col}` 含有非數值型數據，請檢查！")

    return errors