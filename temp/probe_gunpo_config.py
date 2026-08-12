"""
gunpo_main_real.js의 CONFIG 객체 상세 파싱
"""
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("gunpo_main_real.js", "r", encoding="utf-8") as f:
    js = f.read()

# CONFIG 객체 선언 찾기
idx = js.find("SEARCH_COLLECTION_DEFAULT")
if idx != -1:
    print("=== CONFIG snippet around SEARCH_COLLECTION_DEFAULT ===")
    print(js[max(0, idx-400):min(len(js), idx+400)])
