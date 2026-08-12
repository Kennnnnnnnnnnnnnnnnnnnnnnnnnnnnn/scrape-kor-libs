"""
시흥시 Pyxis API 검색 필드 및 추가 매개변수 전수 진단
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

# 검색 성공을 위한 다양한 파라미터 조합
cases = [
    # 1. searchKeyword + searchField
    {"searchKeyword": "python", "searchField": "ALL", "page": 1, "display": 10},
    {"searchKeyword": "python", "searchField": "title", "page": 1, "display": 10},
    # 2. searchKeyword + materialType
    {"searchKeyword": "python", "materialType": "all", "page": 1, "display": 10},
    {"searchKeyword": "python", "material-type": "all", "page": 1, "display": 10},
    # 3. searchKeyword + branch
    {"searchKeyword": "python", "branch": "all", "page": 1, "display": 10},
    # 4. searchKeyword + sort + order
    {"searchKeyword": "python", "sort": "RANK", "order": "DESC", "page": 1, "display": 10},
    # 5. 복합형
    {"searchKeyword": "python", "searchField": "ALL", "materialType": "all", "branch": "all", "page": 1, "display": 10}
]

for i, p in enumerate(cases):
    try:
        r = session.get(url, params=p, headers=HEADERS, timeout=8, verify=False)
        data = r.json()
        total = data.get("data", {}).get("totalCount", 0) if isinstance(data.get("data"), dict) else 0
        print(f"Case {i} -> Status: {r.status_code}, Total: {total}, Resp: {r.text[:150]}")
    except Exception as e:
        print(f"Case {i} -> Error: {e}")
