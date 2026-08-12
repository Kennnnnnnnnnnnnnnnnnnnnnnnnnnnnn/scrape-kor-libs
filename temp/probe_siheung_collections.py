"""
시흥시 Pyxis API 컬렉션 ID 전수 검사
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
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

col_ids = [1, 2, 3, 4, 5, 8, 9]

for cid in col_ids:
    url = f"https://lib.siheung.go.kr/pyxis-api/1/collections/{cid}/search"
    params = {
        "searchKeyword": "python",
        "page": "1",
        "display": "10"
    }
    try:
        r = session.get(url, params=params, headers=HEADERS, timeout=8, verify=False)
        print(f"ColID {cid} -> Status: {r.status_code}, Response: {r.text[:200]}")
    except Exception as e:
        print(f"ColID {cid} -> Error: {e}")
