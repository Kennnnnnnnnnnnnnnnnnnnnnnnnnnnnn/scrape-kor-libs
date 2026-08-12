import requests, urllib3
urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

urls = [
    "https://www.nowonlib.kr/intro/menu/10003/program/30001/searchResultList.do",
    "https://www.nowonlib.kr/intro/menu/10181/program/30012/plusSearchResultList.do",
    "https://www.nowonlib.or.kr/intro/menu/10003/program/30001/searchResultList.do",
    "https://www.nowonlib.or.kr/intro/menu/10181/program/30012/plusSearchResultList.do"
]

params = {
    "searchType": "SIMPLE",
    "searchKeyword": "파친코",
    "searchManageCode": "ALL",
    "searchDisplay": "100"
}

for u in urls:
    try:
        r = requests.get(u, params=params, headers=headers, timeout=5, verify=False)
        print(f"{u} -> status: {r.status_code}, len: {len(r.text)}")
        if r.status_code == 200 and "totalCnt" in r.text or "resultList" in r.text or "bookDataWrap" in r.text:
            print("  ==> MATCH FOUND!")
    except Exception as e:
        print(f"{u} -> error: {e}")
