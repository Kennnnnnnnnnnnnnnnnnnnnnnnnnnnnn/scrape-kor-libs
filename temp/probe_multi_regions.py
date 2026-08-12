"""
군산시립도서관 & 천안시도서관 실시간 수집 검증기
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 1. 군산시립도서관 (JNET)
print("=== 1. 군산시립도서관 (JNET) ===")
url_gs = "https://lib.gunsan.go.kr/web/menu/10003/program/30001/searchResultList.do"
try:
    r = session.get(url_gs, params={"searchKeyword": "파이썬", "searchType": "SIMPLE"}, headers=HEADERS, timeout=10, verify=False)
    print(f"Status: {r.status_code}, Len: {len(r.text)}, '파이썬' count: {r.text.count('파이썬')}")
    if r.text.count("파이썬") > 1:
        soup = BeautifulSoup(r.text, "html.parser")
        for sel in ["dl.bookDataWrap", "div.book_dataInner", "ul.result_list > li", "table tbody tr"]:
            items = soup.select(sel)
            if items:
                print(f"  Selector '{sel}': {len(items)} items")
                for i, it in enumerate(items[:2]):
                    print(f"    [{i+1}] {it.text.strip()[:100]}")
except Exception as e:
    print(f"Error: {e}")

# 2. 천안시도서관 (KOLAS/DLS)
print("\n=== 2. 천안시도서관 (KOLAS) ===")
url_ca = "https://kolas.cheonan.go.kr/search/index.php"
try:
    r = session.get(url_ca, params={"mod": "wdDataSearch", "act": "search", "searchWord": "파이썬"}, headers=HEADERS, timeout=10, verify=False)
    print(f"Status: {r.status_code}, Len: {len(r.text)}, '파이썬' count: {r.text.count('파이썬')}")
    if r.text.count("파이썬") > 1:
        soup = BeautifulSoup(r.text, "html.parser")
        for sel in ["ul.result_list > li", "div.book_list > ul > li", "table tbody tr", "div.search_list_box"]:
            items = soup.select(sel)
            if items:
                print(f"  Selector '{sel}': {len(items)} items")
                for i, it in enumerate(items[:2]):
                    print(f"    [{i+1}] {it.text.strip()[:100]}")
except Exception as e:
    print(f"Error: {e}")
