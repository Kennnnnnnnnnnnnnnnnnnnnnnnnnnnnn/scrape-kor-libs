"""
경기 주요 미구현 도서관 (부천시, 안양시) 메인 검색 경로 분석
"""
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

TARGETS = {
    "부천시": "https://www.bcl.go.kr",
    "안양시": "https://lib.anyang.go.kr"
}

for name, base_url in TARGETS.items():
    print(f"\n=== {name} ({base_url}) 분석 시작 ===")
    try:
        r = requests.get(base_url, headers=HEADERS, timeout=8, verify=False)
        print("  Final URL:", r.url)
        print("  Status:", r.status_code)
        
        soup = BeautifulSoup(r.text, "html.parser")
        
        # 폼 분석
        forms = soup.select("form")
        print(f"  Forms found: {len(forms)}")
        for i, f in enumerate(forms):
            print(f"    Form[{i}] action={f.get('action')} method={f.get('method')}")
            for inp in f.select("input, select"):
                print(f"      <{inp.name}> name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")
                
        # 스크립트 분석
        for j, sc in enumerate(soup.select("script")):
            txt = sc.text
            if any(w in txt for w in ["search", "Search", "action"]):
                print(f"    Script[{j}] has search/action context:")
                for line in txt.split("\n"):
                    if any(w in line for w in ["location", "href", "action", "search"]):
                        print(f"      {line.strip()[:100]}")
                        
    except Exception as e:
        print(f"  Error: {e}")
