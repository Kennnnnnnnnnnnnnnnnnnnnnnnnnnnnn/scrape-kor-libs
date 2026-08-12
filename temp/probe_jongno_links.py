import requests, urllib3, re
urllib3.disable_warnings()
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://lib.jongno.go.kr/menu/subpage/subpage_02/sub01.php"
payload = {"search_value": "파친코", "library": "ALL", "search_type": "normal"}

r = requests.post(url, data=payload, headers=headers, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

for a in soup.select("a[href*='sub']"):
    print("A tag href:", a.get("href"), "| text:", a.text.strip())
