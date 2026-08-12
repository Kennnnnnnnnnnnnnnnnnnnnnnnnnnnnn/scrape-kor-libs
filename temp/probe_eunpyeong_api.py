import requests, urllib3, json
urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'Referer': 'https://www.eplib.or.kr/unified/search.asp'
}

payload = {
    "searchKeyword": "파친코",
    "page": 1,
    "display": 20,
    "selectedLibraries": ["ALL"]
}

r = requests.post("https://www.eplib.or.kr/api/search", json=payload, headers=headers, timeout=12, verify=False)
data = r.json()

print("Eunpyeong Status:", r.status_code)
contents = data.get("contents", {})
items = contents.get("bookList", [])
print("Items:", len(items))

if items:
    item = items[0]
    print("Item 1 keys:", list(item.keys()))
    s_key = item.get("speciesKey", "").split(",")[0].strip()
    m_codes = [mc.strip() for mc in item.get("manageCode", "").split(",") if mc.strip()]
    print(f"speciesKey: {s_key}, manageCodes: {m_codes}")
    
    if m_codes:
        url_det = f"https://www.eplib.or.kr/api/bookDetail/bookCollection/MOMM?speciesKey={s_key}&manageCode={m_codes[0]}"
        r_det = requests.get(url_det, headers=headers, timeout=5, verify=False)
        print("Detail status:", r_det.status_code)
        if r_det.status_code == 200:
            print("Detail JSON:", json.dumps(r_det.json(), ensure_ascii=False)[:500])
