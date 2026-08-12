import requests, urllib3, re
urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

urls = [
    "https://www.jongnolib.or.kr/intro/menu/10003/program/30001/searchResultList.do",
    "https://www.jongnolib.seoul.kr/intro/menu/10003/program/30001/searchResultList.do",
    "https://lib.jongno.go.kr/intro/menu/10003/program/30001/searchResultList.do",
    "https://lib.jongno.go.kr/plus/search/search_result.php"
]

params = {
    "searchType": "SIMPLE",
    "searchCategory": "ALL",
    "searchKey": "ALL",
    "searchLibrary": "ALL",
    "searchKeyword": "파친코"
}

for u in urls:
    try:
        r = requests.get(u, params=params, headers=headers, timeout=5, verify=False)
        print(f"{u} -> status: {r.status_code}, len: {len(r.text)}")
        if r.status_code == 200 and ("bookDataWrap" in r.text or "search_result" in r.text):
            print("  ==> MATCH FOUND!")
    except Exception as e:
        print(f"{u} -> error: {e}")
