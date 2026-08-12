"""
광명시도서관 HTML 내 getDataDetail 비주석 호출부 전체 탐색
"""
with open("gwangmyeong_dls.html", "r", encoding="utf-8") as f:
    txt = f.read()

# 'getDataDetail' 단어를 검색하고 그 주변을 인쇄
import re
matches = list(re.finditer("getDataDetail", txt))
print(f"Total getDataDetail matches: {len(matches)}")

for i, m in enumerate(matches):
    pos = m.start()
    snippet = txt[max(0, pos-100):pos+150]
    # 주석(/* 또는 //) 여부 인근 체크
    is_commented = "/*" in txt[max(0, pos-400):pos] or "//" in txt[max(0, pos-100):pos]
    print(f"Match {i} (Index {pos}, Commented: {is_commented}):")
    print("  ", snippet.strip().replace("\n", " "))
