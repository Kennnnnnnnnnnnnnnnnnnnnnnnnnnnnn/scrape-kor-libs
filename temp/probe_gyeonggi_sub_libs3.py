"""
동대문구립도서관 (www.l4d.or.kr) & 강북구립도서관 (gblib.or.kr) JNET 엔드포인트 탐색
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

targets = [
    ("동대문구립도서관", "https://www.l4d.or.kr/intro/index.do"),
    ("강북구립도서관", "https://www.gblib.or.kr/")
]

for name, url in targets:
    print(f"\n=== [{name}] {url} ===")
    r = session.get(url, headers=HEADERS, timeout=8, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    
    print("Forms:")
    for form in soup.select("form"):
        print(f"  Form action='{form.get('action')}' method='{form.get('method')}' id='{form.get('id')}'")
        for inp in form.select("input, select"):
            print(f"    name='{inp.get('name')}' value='{inp.get('value')}' type='{inp.get('type')}'")
            
    print("JNET/Search Links:")
    for a in soup.select("a"):
        href = a.get("href", "")
        if "jnet" in href.lower() or "search" in href.lower():
            print(f"  Link: '{a.text.strip()[:20]}' -> {href}")
