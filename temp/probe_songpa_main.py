"""
송파구립도서관 메인 검색 구조 분석
"""
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://www.splib.or.kr/intro/index.do"
try:
    r = requests.get(url, headers=HEADERS, timeout=8, verify=False)
    print("Final URL:", r.url)
    print("Status:", r.status_code)
    
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 폼 분석
    forms = soup.select("form")
    print("Forms:", len(forms))
    for i, f in enumerate(forms):
        print(f"  Form[{i}] action={f.get('action')} method={f.get('method')}")
        for inp in f.select("input, select"):
            print(f"    <{inp.name}> name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")
            
    # 스크립트 분석
    for j, sc in enumerate(soup.select("script")):
        txt = sc.text
        if any(w in txt for w in ["search", "Search", "action"]):
            print(f"  Script[{j}] has search/action context:")
            for line in txt.split("\n"):
                if any(w in line for w in ["location", "href", "action", "search"]):
                    print(f"    {line.strip()[:120]}")
                    
except Exception as e:
    print("Error:", e)
