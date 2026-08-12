"""
군포시도서관 Pyxis API 백엔드 호출 규격 검증
"""
import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8'
}

# pyxis-api 후보군
urls = [
    "https://www.gunpolib.go.kr/pyxis-api/1/collections/1/search",
    "https://www.gunpolib.go.kr/pyxis-api/collections/1/search",
    "https://www.gunpolib.go.kr/pyxis-api/1/search"
]

# pyxis api는 GET/POST 둘 다 지원하며 일반적으로 POST JSON 페이로드 사용
payload = {
    "all": "파이썬",
    "allCheck": "true",
    "start": 0,
    "max": 10,
    "searchField": "ALL",
    "searchKeyword": "파이썬"
}

for url in urls:
    print(f"\nAPI URL: {url}")
    # 1. POST 방식 테스트
    try:
        r = requests.post(url, json=payload, headers=HEADERS, timeout=8, verify=False)
        print(f"  POST Status: {r.status_code}, Length: {len(r.text)}")
        if r.status_code == 200 and "success" in r.text:
            print("    [SUCCESS!!!] POST response JSON:")
            print(r.text[:1000])
    except Exception as e:
        print("  POST Error:", e)

    # 2. GET 방식 테스트
    try:
        params = {"q": "파이썬", "max": 10, "searchField": "ALL", "searchKeyword": "파이썬"}
        r = requests.get(url, params=params, headers=HEADERS, timeout=8, verify=False)
        print(f"  GET Status: {r.status_code}, Length: {len(r.text)}")
        if r.status_code == 200:
            print("    [SUCCESS!!!] GET response:")
            print(r.text[:1000])
    except Exception as e:
        print("  GET Error:", e)
