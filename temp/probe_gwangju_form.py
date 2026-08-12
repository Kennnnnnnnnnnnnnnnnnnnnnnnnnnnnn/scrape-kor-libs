"""
광주시 S1T446C461 폼 및 JS 상세 분석
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://lib.gjcity.go.kr/lay1/program/S1T446C461/jnet/resourcessearch/resultList.do"
r = session.get(url, headers=HEADERS, verify=False)

soup = BeautifulSoup(r.text, "html.parser")
form = soup.select_one("form#libSearch2")

if form:
    print("=== libSearch2 Form ===")
    print("action:", form.get("action"))
    print("method:", form.get("method"))
    for inp in form.select("input, select"):
        print(" ", inp.name, "tag:", inp.name, "name:", inp.get("name"), "value:", inp.get("value"))

print("\n=== Scripts ===")
for sc in soup.select("script"):
    if "search" in sc.text.lower() or "submit" in sc.text.lower():
        print(sc.text.strip()[:400])
        print("="*30)
