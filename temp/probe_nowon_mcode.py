import requests, urllib3, json
urllib3.disable_warnings()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://www.nowonlib.kr/'
}

species_key = "1077914"
manage_codes = ["ME", "MF", "MG", "SA", "SB", "SC", "SF", "SH", "SI", "SK", "SL", "SP", "SR", "ST", "SU", "SW", "SX", "SY", "SZ"]

for mcode in manage_codes[:3]:
    url = f"https://www.nowonlib.kr/api/bookDetail/bookCollection/SE?speciesKey={species_key}&manageCode={mcode}"
    r = requests.get(url, headers=headers, timeout=10, verify=False)
    print(f"ManageCode: {mcode} -> status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(json.dumps(data, ensure_ascii=False, indent=2)[:1000])
        print("=" * 60)
