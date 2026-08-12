"""
광주시 S1T446C461 응답 HTML 내용 상세 분석
"""
import requests
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://lib.gjcity.go.kr/lay1/program/S1T446C461/jnet/resourcessearch/resultList.do"
params = {
    "searchType": "SIMPLE",
    "searchCategory": "ALL",
    "searchKey": "ALL",
    "searchLibrary": "ALL",
    "searchKeyword": "파이썬"
}

r = session.get(url, params=params, headers=HEADERS, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

# h2, h3, div.sub_content, p 등
for el in soup.select("h1, h2, h3, h4, div.sub_content, div.contents, p"):
    txt = el.text.strip().replace("\n", " ")
    if len(txt) > 5 and len(txt) < 150:
        print(f"<{el.name}> class={el.get('class', [])}: '{txt}'")
