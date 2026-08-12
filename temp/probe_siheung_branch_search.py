"""
시흥시 Pyxis API 지점 제한 검색 검증
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_SSL_CIPHERS = 'DEFAULT@SECLEVEL=0'
class SslAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context(ciphers=_SSL_CIPHERS)
        ctx.check_hostname = False
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', SslAdapter())
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://lib.siheung.go.kr/',
    'X-Requested-With': 'XMLHttpRequest'
}

url = "https://lib.siheung.go.kr/pyxis-api/1/collections/1/search"

# branch=1 (중앙도서관) 검색 테스트
params_1 = {
    "searchKeyword": "파이썬",
    "page": 1,
    "display": 10,
    "branch": "1"
}

try:
    r = session.get(url, params=params_1, headers=HEADERS, timeout=8, verify=False)
    print("=== Test 1 (branch=1) ===")
    print("Status:", r.status_code)
    data = r.json()
    total = data.get("data", {}).get("totalCount", 0) if isinstance(data.get("data"), dict) else 0
    print("Total:", total)
    if total > 0:
        print("First Title:", data["data"]["list"][0].get("title"))
except Exception as e:
    print("Error 1:", e)

# branch 전체 나열 검색 테스트
params_all = {
    "searchKeyword": "파이썬",
    "page": 1,
    "display": 10,
    "branch": "1,12,2,3,11,10,75,73,81,16"
}
try:
    r = session.get(url, params=params_all, headers=HEADERS, timeout=8, verify=False)
    print("\n=== Test 2 (branch=all list) ===")
    print("Status:", r.status_code)
    data = r.json()
    total = data.get("data", {}).get("totalCount", 0) if isinstance(data.get("data"), dict) else 0
    print("Total:", total)
    if total > 0:
        print("First Title:", data["data"]["list"][0].get("title"))
except Exception as e:
    print("Error 2:", e)
