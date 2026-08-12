"""
시흥시도서관 JSON 설정 파일 직접 획득 검증
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

settings = ["api.json", "search.json", "default.json"]
for s in settings:
    url = f"https://lib.siheung.go.kr/_conf/settings/{s}"
    try:
        r = session.get(url, headers=HEADERS, timeout=8, verify=False)
        print(f"URL: {url} -> Status: {r.status_code}, Length: {len(r.text)}")
        if r.status_code == 200:
            print("=== CONTENT ===")
            print(json.dumps(r.json(), ensure_ascii=False, indent=2)[:1000])
    except Exception as e:
        print("Error:", e)
