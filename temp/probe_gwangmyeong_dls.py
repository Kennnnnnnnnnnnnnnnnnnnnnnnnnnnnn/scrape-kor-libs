"""
광명시도서관 실제 DLS 검색(searchIList) 실시간 검증
"""
import requests
from bs4 import BeautifulSoup
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://gmlib.gm.go.kr/dls_le/index.php"
params = {
    "mod": "wdDataSearch",
    "act": "searchIList",
    "item": "total",
    "word": "파이썬"
}

try:
    r = requests.get(url, params=params, headers=HEADERS, timeout=10, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("gwangmyeong_dls.html", "w", encoding="utf-8") as f:
        f.write(r.text)
        
    soup = BeautifulSoup(r.text, "html.parser")
    
    # 책 제목을 포함할 법한 태그들 탐색
    print("\n=== 제목 태그 분석 ===")
    # 일반적인 DLS 솔루션의 링크 패턴인 detail 이나 view 또는 class=title
    titles = soup.select(".title a, a[href*='searchIDetail'], a[href*='wdBookDetail']")
    if not titles:
        titles = [a for a in soup.select("a") if a.get("href") and "Detail" in a.get("href")]
        
    print(f"Titles found: {len(titles)}")
    for i, t in enumerate(titles[:5]):
        print(f"  [{i}] Title: {t.text.strip()} | Href: {t.get('href')}")
        
    # '파이썬' 단어 카운트
    print("Keyword count:", r.text.count("파이썬"))
except Exception as e:
    print("Error:", e)
