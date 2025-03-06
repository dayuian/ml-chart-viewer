import streamlit as st

def sidebar():
    """側邊欄"""
    st.sidebar.info("請選擇分頁來切換不同功能")

    # 📖 **使用說明**
    with st.sidebar.expander("📖 使用說明", expanded=False):
        st.write("""
        **本應用提供以下功能**：
        1. **檔案管理** - 上傳、查看、管理 `.csv` 檔案。
        2. **數據視覺化** - 選擇適當的圖表來展示數據趨勢。
        3. **數據分析** - 生成數據統計資訊，包括缺失值、極端值。

        **使用步驟**：
        1. **先上傳 CSV 檔案**
        2. **檢視數據摘要，並確認缺失值**
        3. **若需數據清理，可選擇填補缺失值**
        4. **存入數據庫**
        5. **進入圖表視覺化，選擇合適的圖表來分析數據**
        """)

    # 👨‍💻 **開發者資訊**
    with st.sidebar.expander("👨‍💻 開發者資訊", expanded=False):
        st.write("""
        **應用版本**： v1.0.0  
        **開發者**： 余彦志(大宇 / ian)  
        **聯絡方式**： [GitHub](https://github.com/dayuian) | [Email](mailto:dayuian@hotmail.com)  
        **更新日期**： 2025-03-06
        """)

if __name__ == "__main__":
    sidebar()
