"""
울산도서관 결과 상세 구조 파싱
"""
from bs4 import BeautifulSoup
import re

with open("ulsan_raw.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 총 건수
print("=== 1. 총 검색 건수 태그 매칭 ===")
# 검색 결과 수 (e.g. 전체 n건, 도서 n건 등)
found_cnt = soup.find_all(text=re.compile(r'\d+건'))
for t in found_cnt[:5]:
    print(f"  <{t.parent.name}> class={t.parent.get('class')} text='{t.strip()[:100]}'")

# 2. 도서 리스트 요소 클래스 찾기
print("\n=== 2. 도서 리스트 후보 클래스 ===")
div_classes = set()
for tag in soup.select("div, ul, li, dl, dd"):
    cls = tag.get("class")
    if cls:
        div_classes.add(" ".join(cls))
print("Classes:", list(div_classes)[:30])

# 3. 책의 제목이나 저자 등을 포함하는 리스트 항목 정밀 탐색
print("\n=== 3. 도서 항목 구조 탐색 ===")
for tag in soup.select("div, li, dl"):
    text = tag.text
    if "저자" in text and "청구기호" in text and len(text.strip()) < 1200:
        print(f"Found container: <{tag.name}> class={tag.get('class')} id={tag.get('id')}")
        print(f"  HTML preview:")
        print(tag.prettify()[:1000])
        break
