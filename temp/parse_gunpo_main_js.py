"""
군포시 4MB main.js 내 pyxis-api 통신 파라미터 정밀 구문 분석
"""
import re

with open("gunpo_main.js", "r", encoding="utf-8") as f:
    js = f.read()

print("JS Length:", len(js))

# '/search' 나 'collections' 나 'pyxis-api' 가 등장하는 모든 오프셋 탐색
matches = [m.start() for m in re.finditer(r"pyxis-api", js)]
print(f"pyxis-api matches count: {len(matches)}")

for idx, pos in enumerate(matches):
    print(f"\n=== Match {idx} (Pos {pos}) ===")
    # 앞뒤 500바이트 덤프
    snippet = js[max(0, pos-250):pos+600]
    # 읽기 쉽도록 저장
    with open(f"gunpo_api_snippet_{idx}.txt", "w", encoding="utf-8") as out:
        out.write(snippet)
    print(f"Saved snippet to gunpo_api_snippet_{idx}.txt")
    print(snippet[:300].strip().replace("\n", " "))
