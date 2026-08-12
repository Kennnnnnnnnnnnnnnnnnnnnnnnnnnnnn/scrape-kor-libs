"""
서대문구립도서관(lib.sdm.or.kr) 및 광진구립도서관(gwangjinlib.seoul.kr) 도서검색 파싱기
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 1. 서대문구립도서관 (lib.sdm.or.kr)
print("=== 1. 서대문구립도서관 ===")
try:
    r = session.get("https://lib.sdm.or.kr", headers=HEADERS, timeout=8, verify=False)
    print(f"Main Status: {r.status_code}, Len: {len(r.text)}, Final: {r.url}")
    soup = BeautifulSoup(r.text, "html.parser")
    for a in soup.select("a"):
        href = a.get("href", "")
        if "search" in href.lower() or "menu" in href.lower() or "program" in href.lower():
            txt = a.text.strip()
            if 0 < len(txt) < 30:
                print(f"  '{txt}' -> {href}")
except Exception as e:
    print(f"  Error: {e}")

# 2. 광진구립도서관 (gwangjinlib.seoul.kr)
print("\n=== 2. 광진구립도서관 ===")
try:
    r = session.get("https://www.gwangjinlib.seoul.kr", headers=HEADERS, timeout=8, verify=False)
    print(f"Main Status: {r.status_code}, Len: {len(r.text)}, Final: {r.url}")
    soup = BeautifulSoup(r.text, "html.parser")
    for a in soup.select("a"):
        href = a.get("href", "")
        if "search" in href.lower() or "menu" in href.lower() or "program" in href.lower():
            txt = a.text.strip()
            if 0 < len(txt) < 30:
                print(f"  '{txt}' -> {href}")
except Exception as e:
    print(f"  Error: {e}")
