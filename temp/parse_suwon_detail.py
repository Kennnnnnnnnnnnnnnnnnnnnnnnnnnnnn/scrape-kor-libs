"""
수원시 도서관 모바일 검색 결과 HTML 태그 분석
"""
from bs4 import BeautifulSoup
import re

with open("suwon_mobile.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 1. '건' 이나 '결과' 단어가 포함된 태그 찾아보기
print("=== 1. 총 검색 건수 태그 매칭 ===")
found_cnt = soup.find_all(text=re.compile(r'\b\d+건\b|검색\s*결과'))
print(f"Count matches: {len(found_cnt)}")
for t in found_cnt[:5]:
    print(f"  <{t.parent.name}> class={t.parent.get('class')} text='{t.strip()[:100]}'")

# 2. 도서 리스트 요소 클래스 찾기
print("\n=== 2. 도서 리스트/아이템 후보 클래스 ===")
# body 아래의 모든 div, ul, li 클래스 조사
div_classes = set()
for tag in soup.select("div, ul, li"):
    cls = tag.get("class")
    if cls:
        div_classes.add(" ".join(cls))
        
list_classes = [c for c in div_classes if any(w in c.lower() for w in ["list", "book", "item", "search"])]
print("List candidates:", list_classes[:30])

# 3. 책의 제목이나 저자 등을 포함하는 리스트 항목 정밀 탐색
print("\n=== 3. 도서 항목 구조 탐색 ===")
for tag in soup.select("div, li"):
    text = tag.text
    # 첫번째 매칭되는 도서명 느낌의 텍스트가 있는 div/li 탐색
    if "저자" in text and "청구기호" in text and len(text.strip()) < 1500:
        print(f"Found container: <{tag.name}> class={tag.get('class')} id={tag.get('id')}")
        print(f"  HTML preview:")
        print(tag.prettify()[:1000])
        break
