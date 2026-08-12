"""
시흥시 Pyxis API 검색 파라미터 다각도 검사
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
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://lib.siheung.go.kr/pyxis-api/1/collections/1/search"

# 파라미터 후보군 조합 테스트
param_sets = [
    # 1. 안산형 (searchKeyword + page + display)
    {"searchKeyword": "파이썬", "page": 1, "display": 10},
    # 2. Pyxis 표준형 (searchKeyword + max + offset)
    {"searchKeyword": "파이썬", "max": 10, "offset": 0},
    # 3. 상세형 (searchKeyword + page + display + sort + branch + material-type)
    {"searchKeyword": "파이썬", "page": 1, "display": 10, "sort": "RANK", "order": "DESC", "branch": "all", "material-type": "all"},
    # 4. all 파라미터 혼용형
    {"all": "파이썬", "searchKeyword": "파이썬", "page": 1, "display": 10},
]

for i, p in enumerate(param_sets):
    try:
        r = session.get(url, params=p, headers=HEADERS, timeout=8, verify=False)
        print(f"Set {i} -> Status: {r.status_code}, Resp: {r.text[:250]}")
    except Exception as e:
        print(f"Set {i} -> Error: {e}")
