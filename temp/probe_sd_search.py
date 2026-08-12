"""
성동구립도서관 파서 디버그
"""
from bs4 import BeautifulSoup
import re
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://www.sdlib.or.kr/SD/main.do'
}

url = "https://www.sdlib.or.kr/SD/site/search/search00.do"
payload = {
    "cmd_name": "bookandnonbooksearch",
    "search_type": "detail",
    "use_facet": "N",
    "main_type": "Y",
    "search_txt": "파이썬"
}

r = session.get(url, params=payload, headers=HEADERS, timeout=12, verify=False)
soup = BeautifulSoup(r.text, "html.parser")
items = soup.select("div.book_info_w")
print(f"Items: {len(items)}")

for i, item in enumerate(items):
    tit_a = item.select_one("a[href*='species_key'], a[href*='manage_code']")
    print(f"[{i+1}] tit_a: {tit_a.text.strip() if tit_a else 'NONE'}")
