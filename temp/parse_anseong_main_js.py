"""
/library/js/main.js 상세 분석
"""
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

r = requests.get("https://www.anseong.go.kr/library/js/main.js", verify=False)
lines = r.text.split("\n")
for idx, line in enumerate(lines):
    if "bookSearchForm" in line or "searchTxt" in line:
        print(f"Line {idx}:")
        for j in range(max(0, idx-5), min(len(lines), idx+15)):
            print(f"  {lines[j]}")
        print("="*40)
