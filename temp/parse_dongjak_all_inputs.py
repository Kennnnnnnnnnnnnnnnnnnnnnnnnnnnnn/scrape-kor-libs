"""
동작구립도서관 결과 페이지 모든 입력 필드(input, select) 분석
"""
from bs4 import BeautifulSoup

with open("dongjak_search_with_libs.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

inputs = soup.select("input, select")
print(f"Total inputs/selects: {len(inputs)}")
for inp in inputs:
    print(f"  <{inp.name}> name='{inp.get('name')}', value='{inp.get('value')}', id='{inp.get('id')}', type='{inp.get('type')}'")
