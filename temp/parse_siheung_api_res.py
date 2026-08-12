"""
시흥시 Pyxis API 결과 JSON 구조 상세 파싱
"""
import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://lib.siheung.go.kr/'
}

url = "https://lib.siheung.go.kr/pyxis-api/1/collections/1/search"
params = {"all": "k|a|파이썬", "max": 5}

r = session.get(url, params=params, headers=HEADERS, timeout=8, verify=False)
data = r.json()

print("Total count:", data["data"]["totalCount"])
items = data["data"]["list"]

for i, item in enumerate(items):
    print(f"\n=== Item [{i}] ===")
    print("titleStatement:", item.get("titleStatement"))
    print("author:", item.get("author"))
    print("publication:", item.get("publication"))
    print("branchVolumes:", item.get("branchVolumes"))
