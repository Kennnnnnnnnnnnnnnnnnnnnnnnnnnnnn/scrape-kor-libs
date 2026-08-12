"""
안성시 bookSearchForm 제출 JS 함수 분석
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
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

r = session.get("https://www.anseong.go.kr/library/main.do", headers=HEADERS, timeout=8, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

for sc in soup.select("script"):
    txt = sc.text
    if "bookSearchForm" in txt or "searchTxt" in txt or "fn_search" in txt:
        print("=== Script found ===")
        for line in txt.split("\n"):
            if any(w in line for w in ["bookSearchForm", "searchTxt", "location", "submit", "action", "href"]):
                print("  ", line.strip()[:150])
