import requests, urllib3, json, re
urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.nowonlib.kr/'
}

# 1. 1차 검색
url_search = "https://www.nowonlib.kr/api/search"
payload = {
    "searchKeyword": "파친코",
    "page": "1",
    "display": "100" # 100건 수집
}

r = requests.post(url_search, json=payload, headers=headers, timeout=12, verify=False)
data = r.json()

contents = data.get("contents", {})
items = contents.get("bookList", [])

print(f"Total books found: {contents.get('totalCount')}, items in 1st page: {len(items)}")

all_collections = []

for idx, item in enumerate(items, 1):
    raw_title = item.get("originalTitle") or item.get("title", "")
    title = re.sub(r"<[^>]+>", "", raw_title).strip()
    author = item.get("originalAuthor") or item.get("author", "")
    author = re.sub(r"\s*지음|\s*저\.?", "", author).strip()

    species_key = item.get("speciesKey", "")
    manage_codes_str = item.get("manageCode", "")
    if not species_key or not manage_codes_str:
        continue

    # 종 키에 여러 키가 포함되어 있을 수 있음
    s_key = species_key.split(",")[0].strip()
    m_codes = [mc.strip() for mc in manage_codes_str.split(",") if mc.strip()]

    print(f"\n[Book #{idx}] Title: {title} | Author: {author}")
    print(f"  speciesKey: {s_key}, manageCodes count: {len(m_codes)}")

    for mcode in m_codes:
        url_det = f"https://www.nowonlib.kr/api/bookDetail/bookCollection/MOMM?speciesKey={s_key}&manageCode={mcode}"
        try:
            r_det = requests.get(url_det, headers=headers, timeout=5, verify=False)
            if r_det.status_code == 200:
                det_json = r_det.json()
                col_list = det_json.get("contents", {}).get("collectionList", [])
                for col in col_list:
                    lib_name = col.get("libName", "").strip()
                    call_no = col.get("callNo", "").strip()
                    shelf_loc = col.get("shelfLocName", "").strip()
                    if not lib_name.endswith("도서관"):
                        lib_name += "도서관"
                    
                    print(f"    -> 도서관: {lib_name} | 청구기호: {call_no} | 위치: {shelf_loc}")
                    all_collections.append((title, author, lib_name, call_no, shelf_loc))
        except Exception as e:
            pass

print(f"\n총 수집된 소장권수: {len(all_collections)}건")
