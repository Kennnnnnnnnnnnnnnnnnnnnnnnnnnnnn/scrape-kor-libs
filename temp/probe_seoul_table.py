import requests, urllib3
urllib3.disable_warnings()
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url_db = "https://www.unilib.dobong.kr/site/search/search00.do?cmd_name=bookandnonbookdetail&manage_code=SG&species_key=247635468&publish_form_code=MO"
r = requests.get(url_db, headers=headers, verify=False)
soup = BeautifulSoup(r.text, "html.parser")

for table in soup.select("table"):
    print("TABLE IN DOBONG DETAIL:")
    for tr in table.select("tr"):
        print("  TR:", [td.text.strip().replace("\n", " ") for td in tr.select("th, td")])

url_sd = "https://www.sdlib.or.kr/SD/site/search/search00.do?cmd_name=bookandnonbookdetail&manage_code=MA&species_key=217164321&publish_form_code=MO"
r2 = requests.get(url_sd, headers=headers, verify=False)
soup2 = BeautifulSoup(r2.text, "html.parser")

for table in soup2.select("table"):
    print("TABLE IN SEONGDONG DETAIL:")
    for tr in table.select("tr"):
        print("  TR:", [td.text.strip().replace("\n", " ") for td in tr.select("th, td")])
