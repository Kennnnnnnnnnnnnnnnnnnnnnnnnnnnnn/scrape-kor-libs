"""
동작구 common.js 내 libraryList 또는 getLibrary 스크립트 분석
"""
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://lib.dongjak.go.kr/resources/common/js/common.js"
r = session.get(url, headers=HEADERS, verify=False)
print(f"common.js status: {r.status_code}, len: {len(r.text)}")

for line in r.text.split("\n"):
    if any(k in line for k in ["libraryList", "libraryCodes", "getLibrary", "org_code", "manageCode"]):
        print(" ", line.strip()[:140])
