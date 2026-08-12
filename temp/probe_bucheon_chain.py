"""
부천시 alpasq app.js 다운로드 및 REST API 엔드포인트 파싱
"""
import requests
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://alpasq.bcl.go.kr/app.48c71525f6752866ce3e.js"
r = session.get(url, headers=HEADERS, timeout=12, verify=False)
print("Status:", r.status_code, "Length:", len(r.text))

if r.status_code == 200:
    with open("bucheon_app.js", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved bucheon_app.js")

    # API 엔드포인트 주소 패턴 탐색
    matches = re.findall(r'["\'](/api/[^\s\'"]+)["\']', r.text)
    print(f"Found /api/ matches: {len(matches)}")
    for m in set(matches[:30]):
        print("  API:", m)

    # search / keyword 관련 패턴
    matches2 = re.findall(r'.{0,80}search.{0,80}', r.text)
    print(f"\nSearch matches: {len(matches2)}")
    for m in matches2[:15]:
        print("  Match:", m.strip())
