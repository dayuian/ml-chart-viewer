import streamlit as st
from query import search_knowledge_graph

# 📌 設定 Streamlit 介面
def create_ui():
    st.title("🌐 多來源知識圖譜查詢")

    # 📌 應用說明（放在主頁最上方）
    st.markdown("""
    ## 📖 應用說明
    - 本應用可查詢 **Wikidata、DBpedia、Google 知識圖譜**  
    - 支援 **多語言查詢**（台灣華語、英語、日語、韓語）  
    - **請選擇 API 來源** 並輸入關鍵字，即可查詢
    """)

    # 📌 選擇知識圖譜 API
    API_OPTIONS = ["Wikidata", "DBpedia", "Google Knowledge Graph"]
    selected_api = st.selectbox("📡 選擇知識圖譜 API", API_OPTIONS)

    # 📌 選擇語言（僅 Wikidata 需要）
    LANGUAGE_MAPPING = {
        "English": "en",
        "台灣華語": "zh-tw",
        "日本語": "ja",
        "한국어": "ko"
    }
    selected_lang = st.selectbox("🌍 選擇語言（僅 Wikidata 適用）", list(LANGUAGE_MAPPING.keys()))
    lang_code = LANGUAGE_MAPPING[selected_lang]

    # 📌 輸入框
    keyword = st.text_input("🔍 輸入關鍵字（例如：Trump, 蔡英文）")

    # 📌 Google API Key（若選擇 Google Knowledge Graph）
    google_api_key = None
    if selected_api == "Google Knowledge Graph":
        google_api_key = st.text_input("🔑 輸入 Google Knowledge Graph API Key", type="password")

    # 📌 按鈕
    if st.button("查詢"):
        name, description, image_url = search_knowledge_graph(keyword, selected_api, lang_code, google_api_key)

        if name:
            st.markdown(f"**🔹 名稱**: {name}")
            st.markdown(f"**📖 描述**: {description}")
            
            if image_url:
                st.image(image_url, caption=name)
        else:
            st.warning(description)

    # 📌 側邊欄（放開發資訊 & 注意事項）
    with st.sidebar:
        st.header("👨‍💻 開發者資訊")
        st.markdown("""
        - **開發者**: 余彦志 （大宇 / ian）
        - **技術棧**: Streamlit, Python, Wikidata API, DBpedia, Google KG
        - **聯絡方式**: [dayuian@hotmail.com](mailto:dayuian@hotmail.com)
        """)

        st.header("⚠️ 注意事項")
        st.markdown("""
        - **Wikidata** 可能無法查詢所有內容，請切換 API 測試  
        - **Google 知識圖譜 API** 需要 API Key，請前往 [Google Cloud Console](https://console.cloud.google.com/) 申請  
        - **部分查詢結果可能不完整**，請嘗試 **不同名稱或語言**  
        """)

        st.header("📌 資料來源")
        st.markdown("""
        - [Wikidata API](https://www.wikidata.org/wiki/Wikidata:Data_access)  
        - [DBpedia API](https://wiki.dbpedia.org/)  
        - [Google Knowledge Graph API](https://developers.google.com/knowledge-graph/)  
        """)

