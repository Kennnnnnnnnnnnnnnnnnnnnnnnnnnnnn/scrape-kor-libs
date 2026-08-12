import requests, urllib3, json
urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'Referer': 'https://www.nowonlib.kr/'
}

# 1차 검색 첫번째 책 (speciesKey: 1077914)
species_key = "1077914"

urls = [
    "https://www.nowonlib.kr/api/bookDetail/bookCollection/MOMM",
    "https://www.nowonlib.kr/api/bookDetail/bookCollection/SE"
]

for url in urls:
    payload = {"speciesKey": species_key}
    r = requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    print(f"URL: {url} -> status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print("Data sample:")
        print(json.dumps(data, ensure_ascii=False, indent=2)[:1500])
        print("=" * 60)
