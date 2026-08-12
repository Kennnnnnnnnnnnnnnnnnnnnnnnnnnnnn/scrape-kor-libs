"""
순천시립도서관 #searchForm POST 정밀 수집 검증기
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://library.suncheon.go.kr/lib/book/search/searchIndex.do?menuCd=L001001001',
    'Content-Type': 'application/x-www-form-urlencoded'
}

url = "https://library.suncheon.go.kr/lib/book/search/searchIndex.do"
payload = {
    "menuCd": "L001001001",
    "alpha": "",
    "vcindex": "",
    "currentPageNo": "1",
    "nPageSize": "10",
    "searchType": "ALL",
    "search": "파이썬"
}

r = session.post(url, data=payload, headers=HEADERS, timeout=12, verify=False)
count = r.text.count("파이썬")
print("POST Status:", r.status_code, "Len:", len(r.text), "'파이썬' count:", count)

if count > 1:
    soup = BeautifulSoup(r.text, "html.parser")
    with open("suncheon_search_ok.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("★ SUNCHEON POST MATCH SUCCESS! ★ Saved suncheon_search_ok.html!")
    for sel in ["ul.result_list > li", "div.book_list > ul > li", "table tbody tr", "div.search_list_box", "div.result_box", "li.search_item"]:
        items = soup.select(sel)
        if items:
            print(f"  Selector '{sel}': {len(items)} items")
            for i, item in enumerate(items[:3]):
                print(f"    [{i+1}] {item.text.strip()[:100]}")
