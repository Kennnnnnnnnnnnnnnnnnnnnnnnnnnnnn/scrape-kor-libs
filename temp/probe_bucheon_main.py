"""
부천시립도서관 (bcl.go.kr) 메인 및 검색 엔드포인트 탐색
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import re
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
session.mount('http://', SslAdapter())
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print("=== 1. 부천시립도서관 메인 접속 및 리다이렉트 추적 ===")
urls = [
    "http://www.bcl.go.kr",
    "https://www.bcl.go.kr",
    "http://www.bcl.go.kr/site/main/introNew",
    "https://www.bcl.go.kr/site/main/introNew",
    "https://www.bcl.go.kr/site/main/index.do"
]

for url in urls:
    try:
        r = session.get(url, headers=HEADERS, timeout=8, verify=False, allow_redirects=True)
        print(f"  {url} -> Status: {r.status_code}, Final URL: {r.url}, Len: {len(r.text)}")
        if r.status_code == 200 and len(r.text) > 2000:
            soup = BeautifulSoup(r.text, "html.parser")
            forms = soup.select("form")
            print(f"    Forms count: {len(forms)}")
            for i, form in enumerate(forms[:5]):
                print(f"      Form[{i}] action='{form.get('action')}' method='{form.get('method')}' id='{form.get('id')}'")
    except Exception as e:
        print(f"  {url} -> Error: {e}")
