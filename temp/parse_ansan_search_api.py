"""
안산시 app.js 내 bookSearch 관련 API 엔드포인트 추출
"""
import re

with open("ansan_app.js", "r", encoding="utf-8") as f:
    txt = f.read()

# 'bookSearch' 또는 'Search' 단어가 들어간 API 주소 목록 필터링
print("=== bookSearch / search 관련 API ===")
matches_search = re.findall(r"['\"](/api/[a-zA-Z0-9_\-/]*[sS]earch[a-zA-Z0-9_\-/]*)['\"]", txt)
for s in sorted(list(set(matches_search))):
    print("  ", s)
