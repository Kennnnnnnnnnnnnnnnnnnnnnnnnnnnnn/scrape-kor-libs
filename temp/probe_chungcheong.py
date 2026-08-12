"""
청주시립도서관 lib/intro/ 링크 파싱기
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://library.cheongju.go.kr/lib/intro/"
r = session.get(url, headers=HEADERS, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

for a in soup.select("a"):
    href = a.get("href", "")
    txt = a.text.strip()
    if href and href != "#":
        print(f"  '{txt[:20]}' -> {href}")
