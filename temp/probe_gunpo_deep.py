"""
군포시도서관 메인 HTML 스크립트 및 링크 분석
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

r = session.get("https://www.gunpolib.go.kr/", headers=HEADERS, timeout=8, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

print("=== 1. 모든 링크 중 search/자료검색 관련 ===")
for a in soup.select("a"):
    href = a.get("href", "")
    txt = a.text.strip()
    if any(k in href.lower() or k in txt for k in ["search", "검색", "자료", "find"]):
        print(f"  '{txt[:30]}' -> {href}")

print("\n=== 2. 스크립트 태그 내 URL 추출 ===")
for sc in soup.select("script"):
    txt = sc.text
    if any(k in txt.lower() for k in ["search", "result", "location.href"]):
        for line in txt.split("\n"):
            line_s = line.strip()
            if any(k in line_s for k in ["action", "submit", "location", "href", "search"]):
                print(f"  {line_s[:150]}")
