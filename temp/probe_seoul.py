"""
서울도서관 LISOS HTML 구조 분석
"""
import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
url = "https://lib.seoul.go.kr/search/searchDetail.do"
params = {"kwd": "파이썬"}

r = requests.get(url, params=params, headers=HEADERS, timeout=10)
soup = BeautifulSoup(r.text, "html.parser")

# 총 건수
print("=== 총 건수 태그 찾기 ===")
for cls in [".total", ".result", ".count", "#total", "span", "strong", "em"]:
    tags = soup.select(cls)
    for t in tags[:5]:
        if any(w in t.text for w in ["건", "결과", "총"]):
            print(f"  {cls} -> {t.text.strip()}")

# 도서 목록 및 항목
print("\n=== 도서 목록 태그 찾기 ===")
selectors = ["ul.list", "div.list", ".result_list", "#search_result", "tr", "li"]
for sel in selectors:
    items = soup.select(sel)
    book_items = [it for it in items if "저자" in it.text or "청구기호" in it.text]
    if book_items:
        print(f"  Selector: {sel} -> count: {len(book_items)}")
        print(f"    First item text: {book_items[0].text.strip()[:300]}")
        break
