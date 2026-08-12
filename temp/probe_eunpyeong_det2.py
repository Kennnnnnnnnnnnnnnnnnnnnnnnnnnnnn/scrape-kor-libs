import requests, urllib3, json
urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.eplib.or.kr/unified/search.asp'
}

species_key = "534014781"

test_urls = [
    f"https://www.eplib.or.kr/api/bookDetail/bookCollection/MOMM?speciesKey={species_key}&manageCode=ALL",
    f"https://www.eplib.or.kr/api/bookDetail/bookCollection/SE?speciesKey={species_key}&manageCode=ALL",
    f"https://www.eplib.or.kr/api/bookDetail/bookCollection/MOMM?speciesKey={species_key}",
    f"https://www.eplib.or.kr/api/bookDetail/bookInfo?speciesKey={species_key}",
    f"https://www.eplib.or.kr/api/search/detail?speciesKey={species_key}"
]

for u in test_urls:
    r = requests.get(u, headers=headers, timeout=5, verify=False)
    print(f"URL: {u} -> status: {r.status_code}")
    if r.status_code == 200:
        print("Data:", json.dumps(r.json(), ensure_ascii=False)[:300])
        print("=" * 50)
