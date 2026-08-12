import requests, urllib3
urllib3.disable_warnings()
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://lib.jongno.go.kr/menu/subpage/subpage_02/sub01.php?search_value=%ED%8C%8C%EC%B9%9C%EC%BD%94&library=ALL"
r = requests.get(url, headers=headers, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

with open("jongno_search_out.txt", "w", encoding="utf-8") as f:
    f.write(soup.prettify())

print("Saved to jongno_search_out.txt")
