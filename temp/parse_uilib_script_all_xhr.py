"""
의정부 스크립트 파일 내 AJAX/Load 비동기 통신 주소 전수 추출
"""
with open("uijeongbu_all_scripts.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines in scripts text: {len(lines)}")
for idx, line in enumerate(lines):
    if any(w in line for w in ["ajax", "load", "post", "get", "url", "do?"]):
        # 주석 제거 및 간단한 출력
        clean = line.strip()
        if not clean.startswith("//") and not clean.startswith("/*"):
            print(f"  L{idx+1}: {clean[:150]}")
