"""
Type B (plusSearchResultList.do) HTML 상세 구조 분석
"""
import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 평택시 (resultList 구조가 잘 보이는 사이트)
url = "https://www.ptlib.go.kr/intro/menu/10181/program/30012/plusSearchResultList.do"
params = {"searchType": "SIMPLE", "searchCategory": "BOOK", "searchKey": "TITLE", "searchKeyword": "파이썬", "searchOrder": "DESC"}

r = requests.get(url, params=params, headers=HEADERS, timeout=10)
soup = BeautifulSoup(r.text, "html.parser")

items = soup.select("ul.resultList > li")
print(f"Total items: {len(items)}")

if items:
    item = items[0]
    print("\n=== FIRST ITEM RAW HTML (first 3000 chars) ===")
    html_str = str(item)
    print(html_str[:3000])
    
    print("\n=== PARSED STRUCTURE ===")
    # All direct children
    for i, child in enumerate(item.children):
        if hasattr(child, 'name') and child.name:
            cls = child.get('class', [])
            print(f"  child[{i}] <{child.name}> class={cls}")
            # 2nd level children
            for j, sub in enumerate(child.children):
                if hasattr(sub, 'name') and sub.name:
                    sub_cls = sub.get('class', [])
                    txt = sub.text.strip()[:80] if sub.text else ""
                    print(f"    sub[{j}] <{sub.name}> class={sub_cls} text='{txt}'")
