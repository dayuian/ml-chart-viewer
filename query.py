import requests

# 📌 Wikidata 查詢 API
def query_wikidata(entity_id, lang="en"):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{entity_id}.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        entity_data = data["entities"].get(entity_id, {})

        name = entity_data["labels"].get(lang, {}).get("value", "無資料")
        description = entity_data["descriptions"].get(lang, {}).get("value", "無描述")

        # 取得圖片
        image_url = None
        if "P18" in entity_data["claims"]:
            image_info = entity_data["claims"]["P18"][0]["mainsnak"]["datavalue"]["value"]
            image_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{image_info}"

        return name, description, image_url
    else:
        return None, "❌ 查詢失敗，請確認輸入的關鍵字是否正確！", None

# 📌 DBpedia 查詢 API
def query_dbpedia(keyword):
    url = f"https://dbpedia.org/data/{keyword.replace(' ', '_')}.json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        entity_uri = f"http://dbpedia.org/resource/{keyword.replace(' ', '_')}"
        entity_data = data.get(entity_uri, {})

        name = keyword
        description = entity_data.get("http://www.w3.org/2000/01/rdf-schema#comment", [{}])[0].get("value", "無描述")
        image_url = None

        return name, description, image_url
    else:
        return None, "❌ 查詢失敗，請確認輸入的關鍵字是否正確！", None

# 📌 Google Knowledge Graph API
def query_google_kg(keyword, api_key):
    url = f"https://kgsearch.googleapis.com/v1/entities:search?query={keyword}&key={api_key}&limit=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "itemListElement" in data and len(data["itemListElement"]) > 0:
            entity = data["itemListElement"][0]["result"]
            name = entity.get("name", "無資料")
            description = entity.get("description", "無描述")
            image_url = entity.get("image", {}).get("contentUrl", None)

            return name, description, image_url
        else:
            return None, "❌ 查詢失敗，請確認輸入的關鍵字是否正確！", None
    else:
        return None, "❌ 查詢失敗，請稍後再試！", None

# 📌 統一 API 查詢接口
def search_knowledge_graph(keyword, api_source, lang="en", google_api_key=None):
    if api_source == "Wikidata":
        return query_wikidata(keyword, lang)
    elif api_source == "DBpedia":
        return query_dbpedia(keyword)
    elif api_source == "Google Knowledge Graph":
        if not google_api_key:
            return None, "❌ Google API Key 未設置！", None
        return query_google_kg(keyword, google_api_key)
    else:
        return None, "❌ 未知的 API 來源", None
