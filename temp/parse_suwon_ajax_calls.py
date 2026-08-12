"""
수원 모바일 HTML 내 commonAjaxRequest 사용처 분석
"""
import re

with open("suwon_mobile.html", "r", encoding="utf-8") as f:
    html = f.read()

matches = [m.start() for m in re.finditer("commonAjaxRequest", html)]
print(f"Total commonAjaxRequest calls: {len(matches)}")

for i, pos in enumerate(matches):
    chunk = html[pos:pos+400]
    print(f"\n--- Call[{i}] ---")
    # url, method, params 매핑 정보만 추출
    for line in chunk.split("\n"):
        line_s = line.strip()
        if any(w in line_s for w in ["url", "method", "params", "dataType", "success"]):
            print(" ", line_s[:100])
