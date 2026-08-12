import requests, urllib3, json
urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.eplib.or.kr/unified/search.asp'
}

species_key = "534014781"

# 일반적인 구립도서관 manageCode 목록들 테스트
manage_codes = ["MA", "MB", "MC", "MD", "ME", "MF", "MG", "MH", "MI", "MJ", "MK", "ML", "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT", "MU", "MV", "MW", "MX", "MY", "MZ"]

for mcode in manage_codes:
    url = f"https://www.eplib.or.kr/api/bookDetail/bookCollection/MOMM?speciesKey={species_key}&manageCode={mcode}"
    r = requests.get(url, headers=headers, timeout=5, verify=False)
    if r.status_code == 200:
        data = r.json()
        cols = data.get("contents", {}).get("collectionList", [])
        if cols:
            print(f"FOUND IN {mcode}! count: {len(cols)}")
            for c in cols:
                print(f"  libName: {c.get('libName')}, callNo: {c.get('callNo')}, loc: {c.get('shelfLocName')}")
