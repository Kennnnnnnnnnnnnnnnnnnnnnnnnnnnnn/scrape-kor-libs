"""
리다이렉트 스크립트가 포함된 메인 HTML 저장 및 분석
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

def get_text(name, url):
    print(f"\n=== {name} ({url}) ===")
    try:
        r = session.get(url, headers=HEADERS, timeout=8, verify=False)
        print(r.text[:2000])
    except Exception as e:
        print("Error:", e)

get_text("안산시도서관", "http://lib.iansan.net")
get_text("시흥시도서관", "https://lib.siheung.go.kr")
