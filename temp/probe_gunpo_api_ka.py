"""
군포시 Pyxis API 파라미터 조합 탐색기
"""
import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.gunpolib.go.kr/'
}

session.get("https://www.gunpolib.go.kr/", headers={'User-Agent': HEADERS['User-Agent']}, verify=False)

base_url = "https://www.gunpolib.go.kr/pyxis-api/1/collections/1/search"

# 1. GET 방식 다양한 파라미터
get_param_sets = [
    {"all": "1", "kwd": "파이썬"},
    {"all": "1_kwd", "kwd": "파이썬"},
    {"l": "1", "kwd": "파이썬"},
    {"q": "파이썬"},
    {"all": "kwd", "kwd": "파이썬"},
    {"all": "1", "q": "파이썬"},
    {"kwd": "파이썬"},
    {"all": "1", "title": "파이썬"},
    {"all": "1", "kwd": "파이썬", "max": 10},
    {"all": "1", "kwd": "파이썬", "page": 1},
    {"all": "1", "kwd": "파이썬", "offset": 0},
    {"all": "1_kwd", "kwd": "파이썬", "max": 10},
]

print("=== GET Parameter Sets Test ===")
for i, params in enumerate(get_param_sets):
    try:
        r = session.get(base_url, params=params, headers=HEADERS, timeout=8, verify=False)
        print(f"[{i}] {params} -> Status: {r.status_code}, Len: {len(r.text)}")
        if r.status_code == 200 and "success.noRecord" not in r.text and "badRequest" not in r.text:
            print("  ★ SUCCESS MATCH ★:", r.text[:300])
    except Exception as e:
        print(f"[{i}] Error: {e}")

# 2. POST 방식 다양한 JSON body
post_payloads = [
    {"all": "1", "kwd": "파이썬"},
    {"all": "1_kwd", "kwd": "파이썬"},
    {"all": "1", "kwd": "파이썬", "max": 10, "offset": 0},
    {"all": "1_kwd", "kwd": "파이썬", "max": 10, "offset": 0},
    {"all": "1", "kwd": "파이썬", "pageSize": 10, "page": 1},
    {"all": "1", "kwd": "파이썬", "sort": "title", "max": 10},
]

print("\n=== POST Payload Sets Test ===")
for i, payload in enumerate(post_payloads):
    try:
        r = session.post(base_url, json=payload, headers=HEADERS, timeout=8, verify=False)
        print(f"[{i}] {payload} -> Status: {r.status_code}, Len: {len(r.text)}")
        if r.status_code == 200 and "success.noRecord" not in r.text and "badRequest" not in r.text:
            print("  ★ SUCCESS MATCH ★:", r.text[:300])
    except Exception as e:
        print(f"[{i}] Error: {e}")
