"""
의왕시도서관 검색 스크립트 분석 및 실시간 검증
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

# 1. 메인 접속하여 스크립트 내 검색 URL 패턴 추출
r = session.get("https://www.uwlib.or.kr/intro/index.do", headers=HEADERS, timeout=8, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

print("=== 스크립트 내 검색 관련 코드 분석 ===")
for idx, sc in enumerate(soup.select("script")):
    txt = sc.text
    if any(w in txt for w in ["searchForm", "search", "action", "submit"]):
        for line in txt.split("\n"):
            line_s = line.strip()
            if any(w in line_s for w in ["action", "submit", "location", "searchWord", "Form"]):
                print(f"  Script[{idx}]: {line_s[:150]}")

# 2. 다양한 검색 URL 후보 테스트
print("\n=== 검색 URL 후보 테스트 ===")
candidates = [
    "https://www.uwlib.or.kr/intro/search/resultList.do",
    "https://www.uwlib.or.kr/intro/search/resultList.do?searchType=SIMPLE&searchCategory=ALL&searchField=ALL&searchWord=%ED%8C%8C%EC%9D%B4%EC%8D%AC",
    "https://www.uwlib.or.kr/search/tot/result?searchType=SIMPLE&searchWord=%ED%8C%8C%EC%9D%B4%EC%8D%AC",
    "https://www.uwlib.or.kr/kolaseek/search/searchResultList.do?searchKeyword=%ED%8C%8C%EC%9D%B4%EC%8D%AC",
]

for url in candidates:
    try:
        r = session.get(url, headers=HEADERS, timeout=8, verify=False)
        kwd_count = r.text.count("파이썬") if r.status_code == 200 else 0
        print(f"  {url[:80]} -> Status: {r.status_code}, Len: {len(r.text)}, '파이썬': {kwd_count}")
    except Exception as e:
        print(f"  {url[:80]} -> Error: {e}")
