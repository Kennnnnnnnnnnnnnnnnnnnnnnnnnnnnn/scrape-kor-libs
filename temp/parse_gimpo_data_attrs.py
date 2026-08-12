"""
김포시도서관 결과 HTML 내 data-callno 속성이 포함된 태그 분석
"""
from bs4 import BeautifulSoup

with open("gimpo_real_result.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# data-callno 속성이 있는 모든 태그 탐색
tags = soup.select("[data-callno]")
print(f"Tags with data-callno: {len(tags)}")

for idx, tag in enumerate(tags[:12]):
    print(f"\n[{idx}] tag={tag.name} class={tag.get('class')}:")
    print(f"  data-libname: {tag.get('data-libname')}")
    print(f"  data-callno: {tag.get('data-callno')}")
    print(f"  data-titleinfo: {tag.get('data-titleinfo')}")
    print(f"  data-specieskey: {tag.get('data-specieskey')}")
