"""
군포 main.js 정확히 다운로드 및 분석
"""
import requests
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://www.gunpolib.go.kr/main.js"
r = session.get(url, headers=HEADERS, timeout=10, verify=False)
print("Status:", r.status_code, "Length:", len(r.text))

if r.status_code == 200:
    with open("gunpo_main_real.js", "w", encoding="utf-8") as f:
        f.write(r.text)

    # API 패턴 탐색
    matches = re.findall(r'.{0,100}/[a-zA-Z0-9_-]+/api/.{0,100}', r.text)
    print(f"API matches: {len(matches)}")
    for m in matches[:15]:
        print(" ", m.strip())

    # search / collection 패턴
    matches2 = re.findall(r'.{0,80}collections.{0,80}', r.text)
    print(f"Collections matches: {len(matches2)}")
    for m in matches2[:15]:
        print(" ", m.strip())
