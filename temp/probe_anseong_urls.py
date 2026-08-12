"""
안성시 도서관(anseong.go.kr/library/) 메인 및 검색 페이지 접속 분석
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import sys

sys.stdout.reconfigure(encoding='utf-8')
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

urls = [
    "https://www.anseong.go.kr/library/",
    "https://www.anseong.go.kr/library/main.do",
    "https://lib.anseong.go.kr/",
    "https://www.anseong.go.kr/portal/library/index.do"
]

for url in urls:
    try:
        r = session.get(url, headers=HEADERS, timeout=8, verify=False, allow_redirects=True)
        print(f"  {url} -> Status: {r.status_code}, Final URL: {r.url}, Length: {len(r.text)}")
    except Exception as e:
        print(f"  {url} -> Error: {e}")
