"""
연천군 성공 결과 html 상세 파싱 분석
"""
from bs4 import BeautifulSoup
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("yeoncheon_success_1.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 결과 건수
cnt_tag = soup.select_one("span.totalCount, strong.totalCount, em.count, span.searchTotal, p.total")
print(f"Total count tag: {cnt_tag.text.strip() if cnt_tag else 'None'}")

# 항목 리스트 후보
for sel in ["ul.listWrap > li", "div.bookData", "dl.bookDataWrap", "tr.resultListItem", "div.bookList li", "div.resultItem"]:
    items = soup.select(sel)
    if items:
        print(f"Selector '{sel}': {len(items)} items")

# 첫번째 3개 항목 구조 출력
items = soup.select("ul.listWrap > li:not(.noResultNote), div.bookData, dl.bookDataWrap")
if not items:
    # 모든 li나 div 검색
    items = soup.select("ul > li, div.book_dataInner")

print(f"\nItems found: {len(items)}")

for i, item in enumerate(items[:3]):
    print(f"\n=== Item [{i}] ===")
    print("Text:", item.get_text(separator="|", strip=True)[:200])
    for ch in item.find_all(recursive=False):
        print(f"  <{ch.name}> class={ch.get('class', [])}: '{ch.get_text(strip=True)[:80]}'")
