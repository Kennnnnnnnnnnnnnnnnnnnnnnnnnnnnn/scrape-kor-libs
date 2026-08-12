"""
동작구 /dj/intro/search/index.do 검색 실시간 검증
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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Referer': 'https://lib.dongjak.go.kr/dj/index.do'
}

# 1. 메인 세션 형성
r_main = session.get("https://lib.dongjak.go.kr/dj/index.do", headers=headers, verify=False)

url = "https://lib.dongjak.go.kr/dj/intro/search/index.do"

# GET 테스트
params = {
    "menu_idx": "111",
    "booktype": "BOOK",
    "search_type": "ALL",
    "search_text": "파이썬"
}

print("=== GET /dj/intro/search/index.do ===")
r_get = session.get(url, params=params, headers=headers, timeout=12, verify=False)
print("GET Status:", r_get.status_code, "Len:", len(r_get.text), "'파이썬' count:", r_get.text.count("파이썬"))

# POST 테스트
payload = {
    "menu_idx": "111",
    "booktype": "BOOK",
    "search_type": "ALL",
    "search_text": "파이썬"
}

print("\n=== POST /dj/intro/search/index.do ===")
r_post = session.post(url, data=payload, headers=headers, timeout=12, verify=False)
print("POST Status:", r_post.status_code, "Len:", len(r_post.text), "'파이썬' count:", r_post.text.count("파이썬"))

res_text = r_get.text if r_get.text.count("파이썬") > 1 else r_post.text
if res_text.count("파이썬") > 1:
    with open("dongjak_search_ok.html", "w", encoding="utf-8") as f:
        f.write(res_text)
    print("Saved dongjak_search_ok.html!")

    soup = BeautifulSoup(res_text, "html.parser")
    # 항목 리스트 추출
    for sel in ["dl.bookDataWrap", "div.resultItem", "li.resultListItem", "tr.resultListItem", "table tbody tr", "ul.book-list > li", "div.book-info", "div.item-info"]:
        items = soup.select(sel)
        if items:
            print(f"  Selector '{sel}': {len(items)} items")
