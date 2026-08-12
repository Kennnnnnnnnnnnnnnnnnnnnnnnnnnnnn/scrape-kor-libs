"""
성북구립도서관 결과 상세 구조 파싱 (Type B)
"""
from bs4 import BeautifulSoup

with open("seongbuk_brief_2.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 총 건수
# Type B 솔루션에서는 총 건수를 표시하는 strong 이나 class 등을 확인
print("=== 총 건수 태그 찾기 ===")
for cls in [".total", ".result", ".count", "strong.highlight", "em"]:
    tags = soup.select(cls)
    for t in tags[:3]:
        print(f"  {cls} -> {t.text.strip()}")

# 도서 목록 (Type B: ul.resultList > li)
items = soup.select("ul.resultList > li")
print(f"\nBook items count (ul.resultList > li): {len(items)}")

if items:
    print("\n=== FIRST ITEM HTML ===")
    print(items[0].prettify()[:1500])
