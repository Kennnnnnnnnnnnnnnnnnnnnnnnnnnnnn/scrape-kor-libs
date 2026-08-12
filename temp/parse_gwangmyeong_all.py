"""
광명시도서관 결과 페이지 모든 입력 필드 및 링크 구조 분석
"""
from bs4 import BeautifulSoup

with open("gwangmyeong_search.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("=== 1. 모든 input 태그 ===")
inputs = soup.select("input, select")
for inp in inputs:
    print(f"  <{inp.name}> name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")

print("\n=== 2. 클래스명 분석 ===")
classes = set()
for tag in soup.find_all(True):
    cls = tag.get("class")
    if cls:
        classes.add(" ".join(cls))
print("Classes:", list(classes)[:30])
