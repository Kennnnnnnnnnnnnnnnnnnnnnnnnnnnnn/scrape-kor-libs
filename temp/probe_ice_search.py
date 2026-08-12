"""
IncheonEducationScraper 파싱 및 레지스트리 검증 스크립트
"""
from scrapers.incheon import IncheonEducationScraper
import requests
from bs4 import BeautifulSoup
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://lib.ice.go.kr/ice/index.do'
}

url = "https://lib.ice.go.kr/ice/intro/search/index.do"
params = {
    "menu_idx": "113",
    "booktype": "BOOK",
    "search_type": "ALL",
    "search_text": "파이썬"
}

r = session.get(url, params=params, headers=HEADERS, timeout=12, verify=False)
print("GET Status:", r.status_code, "Len:", len(r.text), "'파이썬' count:", r.text.count("파이썬"))

soup = BeautifulSoup(r.text, "html.parser")
cnt_tag = soup.select_one("span.total, div.total-count, span.num")
print("Count tag:", cnt_tag.text if cnt_tag else "None")

# 파싱 태그 분석
for sel in ["table tbody tr", "ul.result-list > li", "div.book-item", "div.search-list > ul > li"]:
    items = soup.select(sel)
    if items:
        print(f"  Selector '{sel}': {len(items)} items")
        for i, item in enumerate(items[:3]):
            print(f"    [{i+1}] {item.text.strip()[:120]}")
