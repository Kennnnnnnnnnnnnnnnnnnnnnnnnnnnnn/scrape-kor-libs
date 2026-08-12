import requests, urllib3, re
urllib3.disable_warnings()
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://lib.jongno.go.kr/menu/subpage/subpage_02/sub01.php"

# POST 방식 테스트
payloads = [
    {"search_value": "파친코", "library": "ALL", "search_type": "normal"},
    {"stx": "파친코"},
    {"search_text": "파친코"}
]

for p in payloads:
    r = requests.post(url, data=p, headers=headers, verify=False)
    print(f"POST {p} -> status: {r.status_code}, len: {len(r.text)}")
    soup = BeautifulSoup(r.text, "html.parser")
    # 파친코가 텍스트에 포함되어 있는지
    if "파친코" in r.text or "파친코" in r.content.decode('utf-8', 'ignore'):
        print("  ==> MATCH FOUND in POST!")
