"""
동작구 main.js 및 main_default.js 상세 분석
"""
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

urls = [
    "https://lib.dongjak.go.kr/resources/homepage/dj/js/main.js",
    "https://lib.dongjak.go.kr/resources/homepage/dj/js/main_default.js"
]

for url in urls:
    r = session.get(url, headers=HEADERS, verify=False)
    print(f"=== {url} (Len: {len(r.text)}) ===")
    for line in r.text.split("\n"):
        if any(k in line for k in ["search", "mainSearchForm", "location", "href", "action", "submit"]):
            print(" ", line.strip()[:150])
