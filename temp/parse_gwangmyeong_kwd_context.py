"""
광명시도서관 HTML 내 '파이썬' 단어 주변 문맥 정밀 추출
"""
import re

with open("gwangmyeong_dls.html", "r", encoding="utf-8") as f:
    html = f.read()

# '파이썬' 단어의 모든 매치 위치 덤프
matches = [m.start() for m in re.finditer("파이썬", html)]
print(f"Total '파이썬' matches: {len(matches)}")

for i, pos in enumerate(matches):
    print(f"\nMatch {i} (Index {pos}):")
    # 앞뒤 180바이트 덤프
    snippet = html[max(0, pos-140):pos+180]
    print(snippet.strip().replace("\n", " "))
