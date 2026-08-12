"""
동작구 메인 mainSearchForm 전송 JS 정밀 분석
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

r = session.get("https://lib.dongjak.go.kr/dj/index.do", headers=HEADERS, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

for sc in soup.select("script"):
    txt = sc.text
    if "mainSearchForm" in txt:
        print("=== mainSearchForm script ===")
        print(txt.strip())
