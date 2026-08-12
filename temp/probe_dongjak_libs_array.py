"""
searchLib 하위 모든 li, input, label 파싱
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://lib.dongjak.go.kr/dj/intro/search/index.do?menu_idx=111"
r = session.get(url, headers=HEADERS, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

for div in soup.select("div.searchLib"):
    print("\n=== searchLib:", div.get("class"), "===")
    for li in div.select("li, label, input"):
        txt = li.text.strip()
        val = li.get("value")
        inp_id = li.get("id")
        name = li.get("name")
        print(f"  <{li.name}> name={name} val={val} id={inp_id} text='{txt}'")
