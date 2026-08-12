"""
양주시 결과 HTML 내 분관 지점 코드 및 목록 추출
"""
from bs4 import BeautifulSoup

with open("yangju_real_result.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("=== 1. searchLibraryArr 또는 지점 checkbox 탐색 ===")
inputs = soup.select("input[name*='LibraryArr'], input[name*='searchLibrary'], checkbox")
print(f"Inputs found: {len(inputs)}")
for inp in inputs:
    print(f"  Input: name='{inp.get('name')}' value='{inp.get('value')}' type='{inp.get('type')}' id='{inp.get('id')}'")

print("\n=== 2. 모든 select 및 option 태그 중 도서관 지점명 매핑 탐색 ===")
selects = soup.select("select")
for sel in selects:
    name = sel.get("name", "")
    id_val = sel.get("id", "")
    print(f"Select: name='{name}' id='{id_val}'")
    for opt in sel.select("option"):
        print(f"  Option: value='{opt.get('value')}' text='{opt.text.strip()}'")
