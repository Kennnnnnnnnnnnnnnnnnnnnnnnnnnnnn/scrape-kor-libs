"""
부천시 /api/search JSON 응답 구조 상세 분석
"""
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("bucheon_api_post.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Result code:", data.get("result", {}).get("code"))
contents = data.get("contents", {})
print("Total count:", contents.get("totalCount"))

items = contents.get("bookList", [])
if not items:
    items = contents.get("list", [])
if not items:
    items = contents.get("resultList", [])

print(f"Items count: {len(items)}")

# contents 객체의 모든 키 출력
print("Contents keys:", list(contents.keys()))

# items 구조 출력
for i, item in enumerate(items[:3]):
    print(f"\n=== Item [{i}] ===")
    if isinstance(item, dict):
        for k, v in item.items():
            print(f"  {k}: {str(v)[:100]}")
