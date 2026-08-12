import requests, urllib3, json
urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'Referer': 'https://www.nowonlib.kr/'
}

# 1차 검색 첫번째 책 key 정보
book_key = "1112736"
species_key = "1077914"
isbn = "9788970129815"

# 여러 가능성이 있는 상세 API 엔드포인트 테스트
endpoints = [
    "https://www.nowonlib.kr/api/search/detail",
    "https://www.nowonlib.kr/api/book/detail",
    "https://www.nowonlib.kr/api/search/holding",
    "https://www.nowonlib.kr/api/search/location",
    "https://www.nowonlib.kr/api/holdingInfo"
]

for ep in endpoints:
    payloads = [
        {"speciesKey": species_key, "bookKey": book_key, "isbn": isbn},
        {"speciesKey": species_key},
        {"bookKey": book_key}
    ]
    for p in payloads:
        try:
            r = requests.post(ep, json=p, headers=headers, timeout=5, verify=False)
            if r.status_code == 200:
                print(f"SUCCESS: {ep} with payload {p}")
                print(json.dumps(r.json(), ensure_ascii=False)[:300])
                print("-" * 50)
        except Exception as e:
            pass
