import requests, urllib3, re
urllib3.disable_warnings()
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 도봉 상세 페이지
url_db = "https://www.unilib.dobong.kr/site/search/search00.do?cmd_name=bookandnonbooksearch&search_type=detail&manage_code=SG&species_key=247635468&publish_form_code=MO"
r_db = requests.get(url_db, headers=headers, verify=False)
soup_db = BeautifulSoup(r_db.text, "html.parser")
print("=== Dobong Detail Page text sample ===")
print(soup_db.text[:1500])

# 성동 상세 페이지
url_sd = "https://www.sdlib.or.kr/SD/site/search/search00.do?cmd_name=bookandnonbooksearch&search_type=detail&manage_code=MA&species_key=217164321&publish_form_code=MO"
r_sd = requests.get(url_sd, headers=headers, verify=False)
soup_sd = BeautifulSoup(r_sd.text, "html.parser")
print("\n=== Seongdong Detail Page text sample ===")
print(soup_sd.text[:1500])
