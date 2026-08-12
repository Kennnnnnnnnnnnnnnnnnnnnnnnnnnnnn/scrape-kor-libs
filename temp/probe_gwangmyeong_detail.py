"""
광명시도서관 상세페이지(searchResultDetail) 기반 청구기호/지점 소장처 검증
"""
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://gmlib.gm.go.kr/dls_le/index.php"
params = {
    "mod": "wdDataSearch",
    "act": "searchResultDetail",
    "dbType": "dan",
    "jongKey": "286296131",
    "bookKey": "286296133"
}

try:
    r = requests.get(url, params=params, headers=HEADERS, timeout=10, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("gwangmyeong_detail.html", "w", encoding="utf-8") as f:
        f.write(r.text)
        
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 1. 테이블 탐색 (소장 도서관 목록)
    print("\n=== 소장 정보 테이블 탐색 ===")
    tables = soup.select("table")
    print(f"Tables found: {len(tables)}")
    for i, table in enumerate(tables):
        headers = [th.text.strip() for th in table.select("th")]
        print(f"  Table[{i}] Headers: {headers}")
        rows = table.select("tbody tr")
        print(f"    Rows count: {len(rows)}")
        for r_idx, row in enumerate(rows[:5]):
            cols = [td.text.strip().replace('\r', '').replace('\n', ' ') for td in row.select("td")]
            print(f"      Row[{r_idx}]: {cols}")
except Exception as e:
    print("Error:", e)
