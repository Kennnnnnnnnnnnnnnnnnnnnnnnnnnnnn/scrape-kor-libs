"""
시흥시 Pyxis API HOME_PAGE_ID 및 Collection ID 교차 매핑 전수 진단
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

# HOME_PAGE_ID 후보: 1 ~ 6
# Collection ID 후보: 1 ~ 4
for hpid in [1, 2, 3, 4, 5, 6]:
    for cid in [1, 2, 3]:
        url = f"https://lib.siheung.go.kr/pyxis-api/{hpid}/collections/{cid}/search"
        params = {
            "searchKeyword": "python",
            "page": 1,
            "display": 10
        }
        try:
            r = session.get(url, params=params, headers=HEADERS, timeout=5, verify=False)
            data = r.json()
            total = data.get("data", {}).get("totalCount", 0) if isinstance(data.get("data"), dict) else 0
            if r.status_code == 200 and data.get("success") and data.get("data") is not None:
                print(f"  [FOUND] HPID: {hpid}, ColID: {cid} -> Total: {total}, success: {data.get('success')}")
                if total > 0:
                    print("    First book:", data["data"]["list"][0].get("title"))
        except Exception as e:
            pass
