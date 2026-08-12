"""
서울도서관 결과 페이지 태그 구조 상세 분석
"""
from bs4 import BeautifulSoup

with open("seoul_brief.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("=== 1. div/ul/li class names inside content ===")
content_div = soup.select_one("#divContents") or soup.select_one(".contents") or soup.select_one("body")
if content_div:
    # 모든 div의 class명
    classes = set()
    for div in content_div.select("div"):
        cls = div.get("class")
        if cls:
            classes.add(" ".join(cls))
    print("Div classes:", list(classes)[:30])

    # ul/li list structures
    print("\n=== 2. List structure check ===")
    lists = content_div.select("ul, ol, table")
    for i, lst in enumerate(lists[:15]):
        cls = lst.get("class", "NoClass")
        id_ = lst.get("id", "NoId")
        children = len(lst.select("li, tr"))
        print(f"List[{i}] tag={lst.name} id={id_} class={cls} items_count={children}")

# 특정 책 정보가 렌더링된 요소 찾아보기
print("\n=== 3. Search target words (e.g. 청구기호, 저자) ===")
for word in ["청구", "저자", "발행", "소장", "도서"]:
    found = soup.find_all(text=lambda text: text and word in text)
    print(f"Word '{word}' found count: {len(found)}")
    for f in found[:3]:
        parent = f.parent
        print(f"  Parent: <{parent.name}> class={parent.get('class')} text='{parent.text.strip()[:100]}'")
