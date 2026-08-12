import requests, urllib3, re
urllib3.disable_warnings()
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://lib.jongno.go.kr/menu/subpage/subpage_02/sub01.php"
payload = {"search_value": "파친코", "library": "ALL", "search_type": "normal"}

r = requests.post(url, data=payload, headers=headers, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

with open("jongno_post_items.txt", "w", encoding="utf-8") as f:
    for idx, item in enumerate(soup.select("li.book_top_info, div.book_name, ul.book_list > li, div.book_dataInner, tr"), 1):
        txt = item.text.strip().replace("\n", " ")
        if len(txt) > 20:
            f.write(f"--- ITEM #{idx} ---\n")
            f.write(txt + "\n\n")

print("Saved to jongno_post_items.txt")
