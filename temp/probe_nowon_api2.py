import requests, urllib3, json
urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 노원구립도서관 소장도서 조회 API 시도
# bookKey: 1112736, speciesKey: 1077914

urls_to_test = [
    "https://www.nowonlib.kr/api/book/locationList",
    "https://www.nowonlib.kr/api/search/locationList",
    "https://www.nowonlib.kr/api/search/bookDetail",
    "https://www.nowonlib.kr/api/book/detail",
    "https://www.nowonlib.kr/api/search/holdList",
    "https://www.nowonlib.kr/api/holding/list",
    "https://www.nowonlib.kr/api/search/holdingList"
]

for url in urls_to_test:
    payload = {"speciesKey": "1077914", "bookKey": "1112736"}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=5, verify=False)
        print(f"{url} -> status: {r.status_code}")
        if r.status_code == 200:
            print("Response:", r.text[:300])
    except Exception as e:
        print(f"{url} -> error: {e}")
