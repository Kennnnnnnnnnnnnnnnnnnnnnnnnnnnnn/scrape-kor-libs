"""
의왕시도서관 검색 결과 HTML 상세 파싱 분석
"""
from bs4 import BeautifulSoup
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("uiwang_result_program.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 1. 다양한 셀렉터로 결과 항목 탐색
selectors = [
    "div.resultItem", "div.bookData", "dl.bookDataWrap", "tr.resultListItem",
    "li.resultItem", "div.bookList", "div.book_info", "div.searchItem",
    "div.resultArea", "div.listArea", "ul.bookList li", "div.book_listBox",
    "div.resultList", "div.resultContents", "table.listType01 tbody tr"
]
for sel in selectors:
    items = soup.select(sel)
    if items:
        print(f"Selector '{sel}': {len(items)} items")

# 2. 파이썬 키워드 인근 구조 분석
idx = html.find("파이썬")
if idx >= 0:
    snippet = html[max(0, idx-300):idx+300]
    print(f"\n=== '파이썬' 인근 구조 ({idx}) ===")
    print(snippet.strip())

# 3. 모든 form 분석
forms = soup.select("form")
print(f"\nForms: {len(forms)}")
for i, form in enumerate(forms[:5]):
    print(f"  Form[{i}] action='{form.get('action')}' id='{form.get('id')}'")

# 4. div > table 구조 분석
tables = soup.select("table")
print(f"\nTables: {len(tables)}")
for i, tbl in enumerate(tables[:10]):
    rows = tbl.select("tr")
    cls = tbl.get("class", [])
    print(f"  Table[{i}] class={cls} rows={len(rows)}")

# 5. a태그 중 detail이 포함된 것들
detail_links = soup.select("a[href*='Detail'], a[href*='detail'], a[onclick*='Detail'], a[onclick*='detail']")
print(f"\nDetail links: {len(detail_links)}")
for i, a in enumerate(detail_links[:5]):
    print(f"  [{i}] text='{a.text.strip()[:50]}' href='{a.get('href', '')[:80]}' onclick='{a.get('onclick', '')[:80]}'")
