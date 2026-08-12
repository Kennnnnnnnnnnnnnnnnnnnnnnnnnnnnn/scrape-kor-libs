"""
시흥시 Pyxis API 헤더/메소드/영어검색어 통합 진단
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3

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

# 1. 헤더 보강 (실제 브라우저와 유사하게 설정)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://lib.siheung.go.kr/',
    'Origin': 'https://lib.siheung.go.kr',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'X-Requested-With': 'XMLHttpRequest'
}

url = "https://lib.siheung.go.kr/pyxis-api/1/collections/1/search"

# 테스트 케이스 정의
# (메소드, 검색어, 파라미터 구조)
test_cases = [
    # GET 방식 영어 검색어
    ("GET", "python", {"searchKeyword": "python", "page": 1, "display": 10}),
    # GET 방식 한글 검색어
    ("GET", "파이썬", {"searchKeyword": "파이썬", "page": 1, "display": 10}),
    # POST 방식 영어 검색어
    ("POST", "python", {"searchKeyword": "python", "page": 1, "display": 10}),
    # POST 방식 한글 검색어
    ("POST", "파이썬", {"searchKeyword": "파이썬", "page": 1, "display": 10}),
]

for i, (method, q, params) in enumerate(test_cases):
    try:
        if method == "GET":
            r = session.get(url, params=params, headers=HEADERS, timeout=8, verify=False)
        else:
            r = session.post(url, json=params, headers=HEADERS, timeout=8, verify=False)
        print(f"Case {i} ({method} '{q}') -> Status: {r.status_code}, Resp: {r.text[:250]}")
    except Exception as e:
        print(f"Case {i} ({method} '{q}') -> Error: {e}")
