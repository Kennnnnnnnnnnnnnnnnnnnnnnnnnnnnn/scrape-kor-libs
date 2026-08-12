"""
동작구립도서관 메인 인덱스(dj/index.do)에서 도서관 코드 옵션값 추출
"""
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://lib.dongjak.go.kr/dj/index.do"
try:
    r = requests.get(url, headers=HEADERS, timeout=8, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    
    select_tags = soup.select("select[name*=library], select[name*=Library], select[id*=library], select[id*=Library]")
    print(f"Library select tags count: {len(select_tags)}")
    for sel in select_tags:
        print(f"Select: name={sel.get('name')}, id={sel.get('id')}")
        options = sel.select("option")
        for opt in options[:15]:
            print(f"  Option: value='{opt.get('value')}', text='{opt.text.strip()}'")
            
    # input[name=libraryCodes] 또는 hidden 태그들도 전부 덤프
    hiddens = soup.select("input[type=hidden]")
    print(f"Hidden inputs: {len(hiddens)}")
    for h in hiddens:
        print(f"  Hidden: name={h.get('name')}, value={h.get('value')}")
except Exception as e:
    print("Error:", e)
