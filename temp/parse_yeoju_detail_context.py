"""
여주시도서관 상세페이지 내 청구기호 문맥 덤프 및 태그 분석
"""
import re

with open("yeoju_detail.html", "r", encoding="utf-8") as f:
    html = f.read()

# '청구기호' 혹은 '청구' 단어의 위치 덤프
matches = [m.start() for m in re.finditer("청구", html)]
print(f"Total '청구' matches: {len(matches)}")

for i, pos in enumerate(matches[:8]):
    print(f"\nMatch {i} (Index {pos}):")
    # 앞뒤 180바이트 덤프
    snippet = html[max(0, pos-140):pos+180]
    print(snippet.strip().replace("\n", " ").replace("\t", " "))
