"""
군포시도서관 Pyxis API 영어 단어(python) 기반 Fuzzing 검증
"""
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://www.gunpolib.go.kr/pyxis-api/1/collections/1/search"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*'
}

combinations = [
    {"all": "python"},
    {"all": "kwd:python"},
    {"all": "title:python"},
    {"searchKeyword": "python"},
    {"searchKeyword": "kwd:python"},
    {"q": "python"},
    {"q": "kwd:python"},
    {"all": "python", "searchField": "ALL"},
    {"all": "kwd:python", "searchField": "ALL"},
    {"all": "kwd:python", "searchKeyword": "python"},
    {"all": "python", "searchKeyword": "python"},
    {"q": "python", "searchField": "ALL"},
    {"q": "kwd:python", "searchField": "ALL"},
    {"all": "python", "max": 10, "start": 0, "sort": "pyxis"},
    {"all": "kwd:python", "max": 10, "start": 0, "sort": "pyxis"},
    {"all": "python", "searchField": "ALL", "max": 10, "start": 0},
    {"all": "kwd:python", "searchField": "ALL", "max": 10, "start": 0}
]

print("=== Pyxis API English Fuzzing ===")
for idx, params in enumerate(combinations):
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=5, verify=False)
        if r.status_code == 200:
            data = r.json()
            total = data.get("data", {}).get("totalCount", 0) if data.get("data") else 0
            code = data.get("code")
            print(f"  Combo[{idx}] {params} -> TotalCount: {total} (Code: {code})")
            if total > 0:
                print(f"    [SUCCESS!!!] Combo[{idx}] is correct!")
                list_data = data.get("data", {}).get("list", [])
                for i, item in enumerate(list_data[:2]):
                    print(f"      [{i}] Title: {item.get('title')} / Author: {item.get('author')}")
        else:
            print(f"  Combo[{idx}] -> Status: {r.status_code}")
    except Exception as e:
        print(f"  Combo[{idx}] -> Error: {e}")
