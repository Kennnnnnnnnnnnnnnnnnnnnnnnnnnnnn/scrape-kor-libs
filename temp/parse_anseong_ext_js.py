"""
안성시 main.do 외부 script src 분석
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

for sc in soup.select("script[src]"):
    src = sc.get("src")
    print("Script src:", src)
    if "common" in src or "main" in src or "search" in src or "lib" in src:
        if not src.startswith("http"):
            src = "https://www.anseong.go.kr" + src
        try:
            r_js = session.get(src, headers=HEADERS, timeout=5, verify=False)
            if "search" in r_js.text.lower() or "book" in r_js.text.lower():
                print(f"  Checking {src}...")
                for line in r_js.text.split("\n"):
                    if any(w in line for w in ["bookSearchForm", "searchTxt", "searchView.do", "searchList.do", "location.href"]):
                        print("    Match:", line.strip()[:150])
        except Exception as e:
            pass
