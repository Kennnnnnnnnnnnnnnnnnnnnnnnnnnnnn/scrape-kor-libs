"""
유성구립도서관 메인페이지 스크립트 요소 분석
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

_SSL_CIPHERS = 'DEFAULT@SECLEVEL=0'
class SslAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context(ciphers=_SSL_CIPHERS)
        ctx.check_hostname = False
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', SslAdapter())

url = "https://lib.yuseong.go.kr"
r = session.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=10, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

print("=== SCRIPTS ===")
scripts = soup.select("script")
for i, s in enumerate(scripts):
    txt = s.text
    if any(w in txt for w in ["search", "Search", "vSrchText", "mainSearch"]):
        print(f"Script[{i}] matches keywords:")
        lines = txt.split("\n")
        for line in lines:
            if any(w in line for w in ["action", "submit", "href", "search"]):
                print(f"  {line.strip()[:120]}")
