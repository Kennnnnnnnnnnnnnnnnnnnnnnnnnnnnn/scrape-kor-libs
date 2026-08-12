"""
유성구립도서관 HTML 태그 및 텍스트 정밀 탐색
"""
from bs4 import BeautifulSoup
import re

with open("yuseong_brief_2.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

print("=== 1. 모든 div 및 ul의 class ===")
for div in soup.select("div, ul")[:50]:
    cls = div.get("class")
    if cls:
        print(f"<{div.name}> class={cls}")

print("\n=== 2. '파이썬' 단어가 포함된 텍스트와 부모 태그 ===")
found = soup.find_all(text=re.compile("파이썬"))
print(f"Total '파이썬' texts: {len(found)}")
for f in found[:10]:
    print(f"  Parent: <{f.parent.name}> class={f.parent.get('class')} id={f.parent.get('id')} text='{f.strip()[:100]}'")
