import streamlit as st
from views.file_management import file_management_page
from views.visualization import visualization_page
from views.analysis_ui import analysis_ui
from data.repo import init_db
from sidebar import sidebar


def main():
    st.set_page_config(page_title="📊 數據分析與可視化平台", layout="wide")
    sidebar()
    st.title("📊 數據分析與可視化平台")
    
    tab1, tab2, tab3 = st.tabs(["📂 檔案管理", "📊 數據視覺化", "📈 數據分析"])
    
    with tab1:
        file_management_page()
    with tab2:
        visualization_page()
    with tab3:
        analysis_ui()

if __name__ == "__main__":
    init_db()  # 確保資料庫初始化
    main()