import requests, urllib3, re
urllib3.disable_warnings()
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://lib.jongno.go.kr/menu/subpage/subpage_02/sub01.php?library=ALL&search_type=normal&search_value=%ED%8C%8C%EC%B9%9C%EC%BD%94"
r = requests.get(url, headers=headers, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

with open("jongno_html2.txt", "w", encoding="utf-8") as f:
    f.write(soup.prettify()[:3000])

print("Saved to jongno_html2.txt")
