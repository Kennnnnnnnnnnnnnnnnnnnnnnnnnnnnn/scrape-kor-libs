"""
시흥시 Pyxis API 익명 세션 유효성(validate) 검증 및 도서 검색 연동
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

print("=== 1. 익명 세션 유효성 검사 (api/validate) ===")
val_url = "https://lib.siheung.go.kr/pyxis-api/api/validate"
try:
    r = session.get(val_url, headers=HEADERS, timeout=8, verify=False)
    print("Status:", r.status_code)
    print("Cookies:", session.cookies.get_dict())
    print("Response:", r.text)
except Exception as e:
    print("Validate Error:", e)

print("\n=== 2. 세션 유지 상태에서 도서 검색 호출 ===")
search_url = "https://lib.siheung.go.kr/pyxis-api/1/collections/1/search"
params = {
    "searchKeyword": "파이썬",
    "page": 1,
    "display": 10
}
try:
    r = session.get(search_url, params=params, headers=HEADERS, timeout=8, verify=False)
    print("Status:", r.status_code)
    data = r.json()
    print("Success:", data.get("success"))
    print("Total Count:", data.get("data", {}).get("totalCount") if isinstance(data.get("data"), dict) else 0)
    print("Response data type:", type(data.get("data")))
except Exception as e:
    print("Search Error:", e)
