"""
군포시 Pyxis API all=k|a|파이썬 & all=kwd 파라미터 실시간 검증
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

# 세션 접속
session.get("https://www.gunpolib.go.kr/", headers={'User-Agent': HEADERS['User-Agent']}, verify=False)

base_urls = [
    "https://www.gunpolib.go.kr/pyxis-api/1/collections/1/search",
    "https://www.gunpolib.go.kr/pyxis-api/1/collections/2/search",
    "https://www.gunpolib.go.kr/pyxis-api/1/collections/6/search"
]

params_list = [
    {"all": "k|a|파이썬"},
    {"all": "1|a|파이썬"},
    {"all": "kwd|파이썬"},
    {"all": "k|a|파이썬", "max": 10},
    {"all": "1|a|파이썬", "max": 10},
    {"all": "kwd|파이썬", "max": 10},
    {"kwd": "파이썬", "max": 10},
    {"q": "파이썬", "max": 10}
]

for url in base_urls:
    print(f"\n=== Base URL: {url} ===")
    for p in params_list:
        try:
            r = session.get(url, params=p, headers=HEADERS, timeout=6, verify=False)
            print(f"  GET params={p} -> Status: {r.status_code}, Len: {len(r.text)}")
            if r.status_code == 200 and "noRecord" not in r.text and "badRequest" not in r.text:
                print("  ★ SUCCESS! ★ Response:", r.text[:400])
                with open("gunpo_api_success.json", "w", encoding="utf-8") as f:
                    f.write(r.text)
        except Exception as e:
            print(f"  Error: {e}")
