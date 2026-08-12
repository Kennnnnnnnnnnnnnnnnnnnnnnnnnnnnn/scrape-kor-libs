"""
의정부 도서관 HTML 내 '파이썬' 단어 주변 문맥 정밀 추출
"""
import re

with open("uilib_search.html", "r", encoding="utf-8") as f:
    html = f.read()

matches = [m.start() for m in re.finditer("파이썬", html)]
print(f"Total '파이썬' matches: {len(matches)}")

for i, pos in enumerate(matches[:10]):
    print(f"\nMatch {i} (Index {pos}):")
    # 앞뒤 180바이트 덤프
    snippet = html[max(0, pos-140):pos+180]
    print(snippet.strip().replace("\n", " "))
