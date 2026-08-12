"""
시흥시 main.js 내 HOME_PAGE_ID 실제 상수 맵핑값 전수 추출
"""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("siheung_main.js", "r", encoding="utf-8") as f:
    txt = f.read()

# 1. "HOME_PAGE_ID" 뒤에 오는 대입 또는 콜론 기호 및 따옴표 값 매칭
pattern = r"HOME_PAGE_ID\s*[:=]\s*['\"]([^'\"]+)['\"]"
matches = re.findall(pattern, txt)
print("Regex findall results:", matches)

# 2. 인접 영역 덤프를 통한 육안 식별
matches_idx = list(re.finditer("HOME_PAGE_ID", txt))
print(f"Total HOME_PAGE_ID references: {len(matches_idx)}")

# constant("CONFIG", ...) 선언부에 HOME_PAGE_ID 가 하드코딩되어 있는지 검증
config_pos = txt.find('constant("CONFIG"')
if config_pos != -1:
    print("\n=== CONFIG Definition Area ===")
    print(txt[config_pos:config_pos+3000].strip().replace("\n", " "))
