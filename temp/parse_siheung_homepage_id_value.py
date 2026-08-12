"""
시흥시 main.js 내 HOME_PAGE_ID 상수 정의 위치 탐색
"""
import re

with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

# HOME_PAGE_ID : '...' 혹은 "..." 패턴 매칭
matches = re.findall(r"['\"]?HOME_PAGE_ID['\"]?\s*:\s*['\"]([^'\"]+)['\"]", txt)
print("HOME_PAGE_ID values found:", matches)
