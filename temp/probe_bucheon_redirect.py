"""
부천시 introNew 페이지 링크 및 스크립트 상세 분석
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

r = session.get("https://www.bcl.go.kr/site/main/introNew", headers=HEADERS, timeout=10, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

print("=== 1. All Links (a tags) ===")
for a in soup.select("a"):
    href = a.get("href", "")
    txt = a.text.strip()
    if href and not href.startswith("javascript"):
        print(f"  '{txt[:30]}' -> {href}")

print("\n=== 2. All Scripts ===")
for sc in soup.select("script"):
    txt = sc.text
    if any(k in txt.lower() for k in ["search", "location", "go", "url", "href"]):
        for line in txt.split("\n"):
            line_s = line.strip()
            if any(k in line_s.lower() for k in ["location", "href", "action", "search", "url"]):
                print("  ", line_s[:150])
