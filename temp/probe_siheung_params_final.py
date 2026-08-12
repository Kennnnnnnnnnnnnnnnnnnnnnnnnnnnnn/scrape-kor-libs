"""
시흥시 Pyxis API 파라미터 전수 진단기 (max, q, searchField, keyword 조합)
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

# 테스트할 파라미터 조합 케이스들
cases = [
    # Case 0: 기본
    {"searchKeyword": "파이썬", "max": 10},
    # Case 1: q 파라미터 대입
    {"q": "파이썬", "max": 10},
    # Case 2: searchField 지정
    {"searchKeyword": "파이썬", "searchField": "ALL", "max": 10},
    {"searchKeyword": "파이썬", "searchField": "title", "max": 10},
    # Case 3: keyword 파라미터
    {"keyword": "파이썬", "max": 10},
    # Case 4: all 조합
    {"all": "파이썬", "max": 10},
    # Case 5: query 파라미터
    {"query": "파이썬", "max": 10},
    # Case 6: branch 전체 대입
    {"searchKeyword": "파이썬", "max": 10, "branch": "1"},
    # Case 7: q 와 searchField
    {"q": "파이썬", "searchField": "ALL", "max": 10}
]

for i, p in enumerate(cases):
    try:
        r = session.get(url, params=p, headers=HEADERS, timeout=8, verify=False)
        data = r.json()
        total = data.get("data", {}).get("totalCount", 0) if isinstance(data.get("data"), dict) else 0
        print(f"Case {i} -> Params: {list(p.keys())} -> Status: {r.status_code}, Success: {data.get('success')}, Total: {total}, Code: {data.get('code')}")
        if total > 0:
            print("  [FOUND!!!] First book:", data["data"]["list"][0].get("title"))
    except Exception as e:
        print(f"Case {i} -> Error: {e}")
