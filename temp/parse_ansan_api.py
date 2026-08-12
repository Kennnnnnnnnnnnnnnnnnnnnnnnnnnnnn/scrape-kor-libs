"""
안산시 app.js 내 백엔드 API 호출 주소 추출 및 분석
"""
import re

with open("ansan_app.js", "r", encoding="utf-8") as f:
    txt = f.read()

# API 주소 패턴 탐색
print("=== 1. API 주소 후보 탐색 ===")
matches_api = re.findall(r"['\"](/api/[a-zA-Z0-9_\-/]+)['\"]", txt)
print(f"API matches: {len(matches_api)}")
if matches_api:
    unique_apis = sorted(list(set(matches_api)))
    for api in unique_apis[:50]:
        print("  ", api)

print("\n=== 2. Pyxis / pyxis-api 관련 탐색 ===")
matches_pyxis = re.findall(r"['\"](/pyxis[a-zA-Z0-9_\-/]*)['\"]", txt)
print(f"Pyxis matches: {len(matches_pyxis)}")
for p in sorted(list(set(matches_pyxis)))[:30]:
    print("  ", p)

print("\n=== 3. 통합 검색 관련 API 단어 탐색 ===")
# biblios, search, collections 등 단어 주변 탐색
for w in ["biblios", "collections", "searchDetail"]:
    matches_w = list(re.finditer(w, txt))
    print(f"Keyword '{w}' matches: {len(matches_w)}")
    for m in matches_w[:5]:
        pos = m.start()
        print(f"  [{w}] context:", txt[max(0, pos-100):pos+100].strip().replace("\n", " "))
