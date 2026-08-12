"""
동작구립도서관 스크립트 내 검색 AJAX 분석
"""
import re

files = ["common.js", "default.js", "dj_default.js"]

for fn in files:
    print(f"\n=== Analyze File: {fn} ===")
    with open(fn, "r", encoding="utf-8") as f:
        txt = f.read()
    
    # ajax, post, get, url 단어 주변을 덤프
    # 특히 '/search/' 나 '/intro/' 등이 쓰인 문맥을 집중 확인
    lines = txt.split("\n")
    matches = []
    for line in lines:
        if any(w in line for w in ["ajax", "/search/", "SearchResult", "search_text"]):
            matches.append(line.strip()[:150])
            
    print(f"Matches count: {len(matches)}")
    for m in matches[:25]:
        print("  ", m)
