"""
부천시 /api/search REST API 실시간 검증
"""
import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'Referer': 'https://alpasq.bcl.go.kr/search/keyword/%ED%8C%8C%EC%9D%B4%EC%8D%AC'
}

url = "https://alpasq.bcl.go.kr/api/search"

# 1. POST JSON payload
payload = {
    "searchKeyword": "파이썬",
    "page": 1,
    "display": 10,
    "manageCode": "ALL"
}

print("=== POST /api/search ===")
try:
    r_post = session.post(url, json=payload, headers=HEADERS, timeout=10, verify=False)
    print("POST Status:", r_post.status_code)
    print("POST Length:", len(r_post.text))
    print("POST Text snippet:", r_post.text[:300])
    if r_post.status_code == 200:
        with open("bucheon_api_post.json", "w", encoding="utf-8") as f:
            f.write(r_post.text)
except Exception as e:
    print("POST Error:", e)

# 2. GET Query Params
params = {
    "searchKeyword": "파이썬",
    "page": 1,
    "display": 10,
    "manageCode": "ALL"
}

print("\n=== GET /api/search ===")
try:
    r_get = session.get(url, params=params, headers=HEADERS, timeout=10, verify=False)
    print("GET Status:", r_get.status_code)
    print("GET Length:", len(r_get.text))
    print("GET Text snippet:", r_get.text[:300])
    if r_get.status_code == 200:
        with open("bucheon_api_get.json", "w", encoding="utf-8") as f:
            f.write(r_get.text)
except Exception as e:
    print("GET Error:", e)
