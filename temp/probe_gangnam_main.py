"""
강동구립도서관 메인 및 검색 엔드포인트 탐색
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
    "https://www.gdfml.or.kr",
    "https://gdlib.or.kr",
    "https://www.gdlib.or.kr",
    "https://www.gangdonglib.seoul.kr"
]

for url in urls:
    try:
        r = session.get(url, headers=HEADERS, timeout=8, verify=False, allow_redirects=True)
        print(f"URL: {url} -> Status: {r.status_code}, Final: {r.url}, Len: {len(r.text)}")
        if r.status_code == 200 and len(r.text) > 1000:
            soup = BeautifulSoup(r.text, "html.parser")
            print(f"  Forms: {len(soup.select('form'))}")
            for form in soup.select("form"):
                print(f"    Form action: {form.get('action')}")
    except Exception as e:
        print(f"Error: {e}")
