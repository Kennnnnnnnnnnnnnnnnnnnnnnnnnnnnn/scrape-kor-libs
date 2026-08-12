"""
마포구립도서관 사이트 URL 탐색기
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

urls = [
    "https://www.mapo.go.kr/site/main/home",
    "https://www.mapo.go.kr/site/mplib/home",
    "https://mapocenter.mapo.go.kr",
    "https://lib.mapo.go.kr/intro/menu/10003/program/30001/searchResultList.do",
]

for url in urls:
    try:
        r = session.get(url, headers=HEADERS, timeout=6, verify=False)
        print(f"URL: {url[:50]} -> Status: {r.status_code}, Len: {len(r.text)}, Final: {r.url[:60]}")
    except Exception as e:
        print(f"Error: {e}")
