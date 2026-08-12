"""
광주시 419 bytes 및 36970 bytes HTML 내용 상세 분석
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

r1 = session.get("https://lib.gjcity.go.kr/intro/menu/10035/program/30005/searchResultList.do", headers=HEADERS, verify=False)
print("=== 419 bytes text ===")
print(r1.text)

r2 = session.get("https://lib.gjcity.go.kr/lay1/program/S1T446C461/jnet/resourcessearch/resultList.do", headers=HEADERS, verify=False)
soup = BeautifulSoup(r2.text, "html.parser")
print("\n=== S1T446C461 scripts ===")
for sc in soup.select("script"):
    if "search" in sc.text.lower() or "submit" in sc.text.lower() or "action" in sc.text.lower():
        print(sc.text.strip()[:200])
