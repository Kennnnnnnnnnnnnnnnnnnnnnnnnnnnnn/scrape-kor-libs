"""
시흥시도서관 _conf/settings/api.json & default.json 설정파일 덤프
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
HEADERS = {'User-Agent': 'Mozilla/5.0'}

files = ["default.json", "api.json", "search.json"]

for f in files:
    url = f"https://lib.siheung.go.kr/_conf/settings/{f}"
    print(f"\n--- Fetching: {url} ---")
    try:
        r = session.get(url, headers=HEADERS, timeout=8, verify=False)
        print("  Status:", r.status_code)
        if r.status_code == 200:
            print("  Content:")
            print(json.dumps(r.json(), ensure_ascii=False, indent=2)[:800])
    except Exception as e:
        print("  Error:", e)
