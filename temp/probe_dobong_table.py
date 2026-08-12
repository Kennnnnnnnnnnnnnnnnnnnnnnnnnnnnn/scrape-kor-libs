import requests, urllib3
urllib3.disable_warnings()
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://www.unilib.dobong.kr/ndls/bookSearch/getBookInfo.do"
params = {
    "manage_code": "SG",
    "reckey": "247635471",
    "species_key": "247635468"
}

r = requests.get(url, params=params, headers=headers, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

for tr in soup.select("tr"):
    print("TR:", [td.text.strip().replace("\n", " ") for td in tr.select("th, td")])
