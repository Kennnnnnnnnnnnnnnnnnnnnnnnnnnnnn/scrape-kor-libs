"""
bucheon_app.js 내 모든 API 엔드포인트 중 검색(search) 관련 분석
"""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("bucheon_app.js", "r", encoding="utf-8") as f:
    js = f.read()

# /api/로 시작하는 모든 엔드포인트 추출
apis = re.findall(r'["\'](/api/[a-zA-Z0-9_/-]+)["\']', js)
print(f"Total API endpoints found: {len(apis)}")

search_apis = set()
for a in set(apis):
    if any(k in a.lower() for k in ["search", "book", "list", "brief", "detail", "item"]):
        search_apis.add(a)

print(f"\nSearch/Book related APIs ({len(search_apis)}):")
for sa in sorted(search_apis):
    print("  ", sa)
