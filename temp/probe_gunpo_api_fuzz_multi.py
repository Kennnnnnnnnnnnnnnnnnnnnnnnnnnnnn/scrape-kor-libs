"""
군포시도서관 Pyxis API HOME_PAGE_ID 및 Collection ID 전수 다차원 Fuzzing 검출기
"""
import requests
import urllib.parse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/plain, */*'
}

# 테스트 후보군
home_ids = ["1", "2", "3"]
coll_ids = ["1", "2", "3", "4", "5"]
kwd_formats = [
    "1|k|a|파이썬",
    "1|k|a|python",
    "kwd:파이썬",
    "kwd:python",
    "파이썬",
    "python"
]

print("=== Pyxis API Multi-Dimension Fuzzing ===")

success_combos = []

for h_id in home_ids:
    for c_id in coll_ids:
        url = f"https://www.gunpolib.go.kr/pyxis-api/{h_id}/collections/{c_id}/search"
        for kwd in kwd_formats:
            try:
                kwd_enc = urllib.parse.quote(kwd)
                final_url = f"{url}?all={kwd_enc}&max=10&start=0"
                
                r = requests.get(final_url, headers=HEADERS, timeout=3, verify=False)
                if r.status_code == 200:
                    data = r.json()
                    total = data.get("data", {}).get("totalCount", 0) if data.get("data") else 0
                    if total > 0:
                        print(f"  [SUCCESS!!!] h_id={h_id}, c_id={c_id}, kwd={kwd} -> TotalCount: {total}")
                        success_combos.append((h_id, c_id, kwd, total))
            except Exception:
                pass

print(f"\nFuzzing finished. Found success combos: {len(success_combos)}")
