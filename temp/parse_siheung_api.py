"""
시흥시 main.js 내 API 엔드포인트 추출 및 분석
"""
import re

with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

# API 주소 패턴 탐색
# e.g. /api/... 나 /search/... 혹은 http/https 형태의 백엔드 호출
print("=== 1. API 패턴 탐색 ===")
matches_api = re.findall(r"['\"](/api/[a-zA-Z0-9_\-/]+)['\"]", txt)
print(f"API calls found: {len(matches_api)}")
if matches_api:
    # 중복 제거 및 상위 50개 출력
    unique_apis = sorted(list(set(matches_api)))
    for api in unique_apis[:60]:
        print("  ", api)

print("\n=== 2. Pyxis / pyxis 관련 키워드 라인 추출 ===")
# Pyxis 솔루션은 보통 /pyxis-api/ 또는 /pyxis/ 형태를 씁니다.
matches_pyxis = re.findall(r"['\"](/pyxis[a-zA-Z0-9_\-/]*)['\"]", txt)
print(f"Pyxis matches: {len(matches_pyxis)}")
for p in sorted(list(set(matches_pyxis)))[:40]:
    print("  ", p)
