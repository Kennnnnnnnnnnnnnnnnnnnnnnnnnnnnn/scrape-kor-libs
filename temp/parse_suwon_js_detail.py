"""
수원 공용 스크립트 파일 내 AJAX URL 추출
"""
import re

for fname in ["suwon_cloudhomepage.ajax.js", "suwon_cloudhomepage.common.js"]:
    print(f"\n=== {fname} ===")
    with open(fname, "r", encoding="utf-8") as f:
        txt = f.read()
    
    # url: "..." 혹은 url : '...' 패턴 검색
    matches = re.findall(r"url\s*:\s*['\"]([^'\"]+)['\"]", txt)
    print("Found exact URLs:", matches)
    
    # / 로 시작하는 AJAX 주소와 유용한 단어 라인들 출력
    lines = txt.split("\n")
    for line in lines:
        if any(w in line for w in ["ajax", "post", "get", "/search/"]):
            print("Line:", line.strip()[:120])
