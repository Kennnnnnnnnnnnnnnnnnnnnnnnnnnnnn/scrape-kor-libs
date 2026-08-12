"""
구로구립도서관 Pyxis GET 쿼리 파라미터 다각도 테스트
"""
import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*'
}

url = "https://lib.guro.go.kr/pyxis-api/1/collections/1/search"

param_variants = [
    {"q": "파이썬"},
    {"kwd": "파이썬"},
    {"all": "kwd:파이썬"},
    {"all": "파이썬"},
    {"ltype": "all", "kwd": "파이썬"},
    {"ltype": "all", "q": "파이썬"},
    {"sm": "all", "q": "파이썬"},
    {"sm": "all", "kwd": "파이썬"},
    {"target": "all", "kwd": "파이썬"},
    {"query": "파이썬"},
    {"searchKeyword": "파이썬"}
]

for p in param_variants:
    r = session.get(url, params=p, headers=HEADERS, timeout=5, verify=False)
    print(f"Params: {p} -> Status: {r.status_code}, Res: {r.text[:120]}")
