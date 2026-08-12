"""
시흥시 도서관 (lib.siheung.go.kr) Pyxis API 인증 및 엔드포인트 탐색
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
    'Referer': 'https://lib.siheung.go.kr/'
}

# 1. 메인 페이지 세션 쿠키 획득
r_main = session.get("https://lib.siheung.go.kr/", headers={'User-Agent': HEADERS['User-Agent']}, verify=False)
print("Main status:", r_main.status_code)
print("Cookies:", session.cookies.get_dict())

# 2. Pyxis API 엔드포인트 후보들 테스트
endpoints = [
    "https://lib.siheung.go.kr/pyxis-api/1/collections/1/search",
    "https://lib.siheung.go.kr/pyxis-api/1/collections/2/search",
    "https://lib.siheung.go.kr/pyxis-api/2/collections/1/search",
    "https://lib.siheung.go.kr/pyxis-api/1/brief-searches",
    "https://lib.siheung.go.kr/pyxis-api/api/validate"
]

print("\n=== GET 엔드포인트 테스트 ===")
for ep in endpoints:
    try:
        r = session.get(ep, params={"all": "k|a|파이썬", "max": 10}, headers=HEADERS, timeout=8, verify=False)
        print(f"GET {ep} -> Status: {r.status_code}, Len: {len(r.text)}")
        print("  Snippet:", r.text[:200])
    except Exception as e:
        print(f"Error: {e}")
