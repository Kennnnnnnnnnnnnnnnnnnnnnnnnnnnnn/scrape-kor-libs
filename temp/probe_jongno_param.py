import requests, urllib3, re
urllib3.disable_warnings()
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://lib.jongno.go.kr/menu/subpage/subpage_02/sub01.php"
params_list = [
    {"stx": "파친코"},
    {"stx": "파친코", "search_type": "normal"},
    {"search_value": "파친코", "library": "ALL"}
]

for p in params_list:
    r = requests.get(url, params=p, headers=headers, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    items = soup.select(".book_list > li, .book_info, tr")
    print(f"Params {p} -> Status: {r.status_code}, items: {len(items)}, len_text: {len(r.text)}")
    if items:
        print("First item text:", items[0].text.strip()[:200].replace("\n", " "))
