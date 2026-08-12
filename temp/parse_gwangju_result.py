"""
경기도 광주시도서관 검색 결과 HTML 파싱 구조 분석
"""
from bs4 import BeautifulSoup
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("gwangju_result.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 검색 결과 리스트 항목 후보 탐색
selectors = [
    "div.resultList li", "div.searchResultList li", "table.resultList tr",
    "ul.resultList li", "div.bookData", "dl.bookDataWrap",
    "div.book_resultList li", "div.searchList li", "div.book_list li",
    "div.result_list li", "li.resultListItem", "div.resultItem",
    "div.bookListArea li", "div.bookSearchList li"
]
for sel in selectors:
    items = soup.select(sel)
    if items:
        print(f"Selector '{sel}': {len(items)} items found")

# form 분석
forms = soup.select("form")
print(f"\nForms: {len(forms)}")
for i, form in enumerate(forms[:5]):
    print(f"  Form[{i}] action='{form.get('action')}' method='{form.get('method')}' id='{form.get('id')}'")

# 타이틀 키워드 카운트
print(f"\n'파이썬' count: {html.count('파이썬')}")
print(f"'python' count (case-insensitive): {html.lower().count('python')}")

# 테이블 구조 탐색
tables = soup.select("table")
print(f"\nTables: {len(tables)}")
for i, table in enumerate(tables[:5]):
    rows = table.select("tr")
    print(f"  Table[{i}]: {len(rows)} rows, class={table.get('class')}")
    if rows:
        cells = rows[0].select("td, th")
        print(f"    First row: {len(cells)} cells")
        for j, cell in enumerate(cells[:8]):
            print(f"      Cell[{j}]: '{cell.text.strip()[:40]}'")
