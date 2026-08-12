"""
의정부시 도서관 fnMainSearchKeyword 및 main-search-btn 핸들러 본문 상세 덤프
"""
with open("uilib_real_main.html", "r", encoding="utf-8") as f:
    html = f.read()

# fnMainSearchKeyword 또는 main-search-btn 단어 인근 분석
import re
matches = list(re.finditer(r"fnMainSearchKeyword|main-search-btn", html))
print(f"Matches found: {len(matches)}")

for i, m in enumerate(matches):
    pos = m.start()
    print(f"\n=== Match {i} Context ===")
    print(html[max(0, pos-150):pos+600].replace("\n", " ").strip())
