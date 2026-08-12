"""
군포시 도서관 (gunpolib.go.kr) Pyxis API 분석 및 실시간 테스트
"""
import requests
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'Referer': 'https://www.gunpolib.go.kr/'
}

# 1. 메인 페이지 세션 생성
session.get("https://www.gunpolib.go.kr/", headers={'User-Agent': HEADERS['User-Agent']}, verify=False)

# 2. Pyxis API 표준 검색 엔드포인트 후보들 테스트
urls = [
    "https://www.gunpolib.go.kr/pyxis-api/1/collections/1/search",
    "https://www.gunpolib.go.kr/pyxis-api/1/collections/2/search",
    "https://www.gunpolib.go.kr/pyxis-api/2/collections/1/search",
    "https://www.gunpolib.go.kr/pyxis-api/1/search",
    "https://www.gunpolib.go.kr/pyxis-api/1/brief-searches"
]

payload = {
    "all": "kwd",
    "allKeyword": "파이썬",
    "keyword": "파이썬",
    "max": 10,
    "offset": 0
}

for url in urls:
    print(f"\n=== POST {url} ===")
    try:
        r = session.post(url, json=payload, headers=HEADERS, timeout=8, verify=False)
        print(f"Status: {r.status_code}, Length: {len(r.text)}")
        if r.status_code == 200:
            print("Response snippet:", r.text[:300])
    except Exception as e:
        print(f"Error: {e}")

# GET 방식 후보 테스트
get_urls = [
    "https://www.gunpolib.go.kr/pyxis-api/1/collections/1/search?all=kwd&allKeyword=%ED%8C%8C%EC%9D%B4%EC%8D%AC",
    "https://www.gunpolib.go.kr/pyxis-api/1/brief-searches?keyword=%ED%8C%8C%EC%9D%B4%EC%8D%AC"
]

for gurl in get_urls:
    print(f"\n=== GET {gurl} ===")
    try:
        r = session.get(gurl, headers=HEADERS, timeout=8, verify=False)
        print(f"Status: {r.status_code}, Length: {len(r.text)}")
        if r.status_code == 200:
            print("Response snippet:", r.text[:300])
    except Exception as e:
        print(f"Error: {e}")
