"""
울산도서관 총 건수 태그 찾기
"""
from bs4 import BeautifulSoup
import re

with open("ulsan_raw.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

# 전체 텍스트에서 '건' 또는 '결과' 등을 포함하는 태그 검색
text_nodes = soup.find_all(text=True)
for node in text_nodes:
    val = node.strip()
    if val and any(w in val for w in ["결과", "전체", "총"]):
        # 숫자 포함 여부
        if re.search(r'\d+', val) and len(val) < 50:
            print(f"Match: <{node.parent.name}> class={node.parent.get('class')} text='{val}'")
