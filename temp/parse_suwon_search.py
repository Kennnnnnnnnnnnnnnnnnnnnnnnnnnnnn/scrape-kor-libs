"""
수원 search.js 내 AJAX URL 추출
"""
import re

with open("suwon_search.js", "r", encoding="utf-8") as f:
    txt = f.read()

# url: '...' 이나 url : "..." 형태 탐색
matches = re.findall(r"url\s*:\s*['\"]([^'\"]+)['\"]", txt)
print("Exact URLs found:", matches)

lines = txt.split("\n")
for line in lines:
    if any(w in line for w in ["ajax", "post", "get", "url", "search"]):
        print("Line:", line.strip()[:120])
