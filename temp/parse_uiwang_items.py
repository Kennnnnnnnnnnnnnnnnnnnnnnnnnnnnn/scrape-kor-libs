"""
의왕시도서관 Variant 1 검색 결과 HTML 파싱 구조 분석
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
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.uwlib.or.kr/intro/index.do',
    'Content-Type': 'application/x-www-form-urlencoded'
}

session.get("https://www.uwlib.or.kr/intro/index.do", headers=HEADERS, timeout=8, verify=False)

url = "https://www.uwlib.or.kr/jungang/program/searchResultList.do"
payload = {
    "searchType": "SIMPLE",
    "searchCategory": "ALL",
    "searchField": "ALL",
    "searchWord": "파이썬",
    "searchLibrary": "ALL",
    "searchPbLibrary": "ALL",
    "searchSmLibrary": "ALL"
}

r = session.post(url, data=payload, headers=HEADERS, timeout=12, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

# 결과 건수
total_tag = soup.select_one("span.totalCount, strong.totalCount, em.count, span.searchTotal")
print(f"Total tag: {total_tag.text.strip() if total_tag else 'None'}")

# 결과 항목 (li)
items = soup.select("ul.listWrap > li:not(.noResultNote)")
print(f"Result items: {len(items)}")

for i, item in enumerate(items[:5]):
    # 제목
    title_tag = item.select_one("a.title, div.title a, p.title a, strong.title a, a.bookName, span.title a")
    if not title_tag:
        # 대체: 첫 번째 a 태그
        all_a = item.select("a")
        title_tag = all_a[0] if all_a else None
    title = title_tag.text.strip() if title_tag else "None"
    
    print(f"\n[{i}] Title: {title}")
    
    # 하위 구조 전체 출력
    for ch in item.find_all(recursive=False):
        cls = ch.get("class", [])
        tag = ch.name
        txt = ch.text.strip().replace("\n", " ")[:100]
        print(f"  <{tag}> class={cls}: '{txt}'")
