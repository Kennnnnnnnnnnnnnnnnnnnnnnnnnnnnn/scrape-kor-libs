"""
교육청도서관(lib.sen.go.kr) 및 성북구립도서관(sblib.seoul.kr)의 메인 검색 폼/스크립트 분석
"""
import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def analyze_site(name, domain):
    url = f"https://{domain}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        print(f"\n=== [{name}] {domain} ===")
        forms = soup.select("form")
        for i, f in enumerate(forms):
            print(f"  Form[{i}] action={f.get('action')} method={f.get('method')}")
            for inp in f.select("input, select"):
                print(f"    <{inp.name}> name={inp.get('name')} value={inp.get('value')}")
        
        scripts = soup.select("script")
        for i, s in enumerate(scripts):
            txt = s.text
            if any(w in txt for w in ["search", "Search", "searchResult"]):
                print(f"  Script[{i}] matches search keywords:")
                for line in txt.split("\n"):
                    if any(w in line for w in ["action", "submit", "href", "search"]):
                        print(f"    {line.strip()[:100]}")
    except Exception as e:
        print(f"[{name}] Error: {e}")

analyze_site("교육청도서관", "lib.sen.go.kr")
analyze_site("성북구립도서관", "sblib.seoul.kr")
