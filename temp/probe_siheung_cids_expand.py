"""
시흥시 Pyxis API 컬렉션 ID 문자열 및 특수조합 전수 분석
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
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://lib.siheung.go.kr/',
    'X-Requested-With': 'XMLHttpRequest'
}

# 컬렉션 ID 후보군 확대
cids = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "all", "total", "main", "search"]

for cid in cids:
    url = f"https://lib.siheung.go.kr/pyxis-api/1/collections/{cid}/search"
    params = {
        "searchKeyword": "python",
        "page": 1,
        "display": 10
    }
    try:
        r = session.get(url, params=params, headers=HEADERS, timeout=6, verify=False)
        data = r.json()
        total = data.get("data", {}).get("totalCount", 0) if isinstance(data.get("data"), dict) else 0
        if r.status_code == 200 and data.get("success"):
            print(f"ColID {cid} -> Total: {total}, success: {data.get('success')}, message: {data.get('message')}, data_type={type(data.get('data'))}")
            if total > 0:
                print("  [SUCCESS!!!] First book:", data["data"]["list"][0].get("title"))
    except Exception as e:
        pass
