"""
오류 도메인 교정 및 광역/지자체 도서관 검색 주소 다중 검증
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

_SSL_CIPHERS = 'DEFAULT@SECLEVEL=0'
class SslAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context(ciphers=_SSL_CIPHERS)
        ctx.check_hostname = False
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', SslAdapter())
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 도메인 교정 타겟 딕셔너리
DOMAINS_TO_TEST = {
    "군포시": ["www.gunpolib.go.kr", "gunpolib.go.kr"],
    "하남시": ["www.hanamlib.go.kr", "lib.hanam.go.kr"],
    "안성시": ["www.anseong.go.kr/library", "ansengl.go.kr", "lib.anseong.go.kr"],
    "의왕시": ["www.uwlib.or.kr", "uwlib.go.kr", "lib.uw.go.kr"],
    "여주시": ["www.yjlib.go.kr", "yjlib.go.kr"],
    "가평군": ["www.gplib.or.kr", "gplib.go.kr"],
    "이천시": ["www.icheonlib.go.kr", "icheonlib.go.kr"],
    "김포시": ["www.gimpo.go.kr/lib/index.do", "lib.gimpo.go.kr"],
    "파주시": ["www.pajulib.or.kr", "lib.paju.go.kr"],
    "안산시": ["lib.ansan.go.kr", "ansan.go.kr/lib"],
    "의정부시": ["www.uabl.go.kr", "uabl.go.kr"],
    "시흥시": ["lib.siheung.go.kr", "www.siheung.go.kr/library"]
}

# 공통 통합검색 경로 후보군
PATHS = [
    "/intro/menu/10003/program/30001/searchResultList.do",  # jnet A
    "/intro/menu/10181/program/30012/plusSearchResultList.do",  # jnet B
    "/search/searchDetail.do",  # kolas A
    "/search/tot/result.do",  # kolas B
    "/search/search_detail.do",
    "/main/searchBrief",
    "/web/menu/10075/program/30005/searchResultList.do"  # 유성구립(LISOS)
]

results = {}

for name, domains in DOMAINS_TO_TEST.items():
    results[name] = []
    print(f"\n--- {name} 검증 시작 ---")
    for dom in domains:
        for path in PATHS:
            # 프로토콜 포함
            url = dom if dom.startswith("http") else f"https://{dom}"
            # 경로가 중복되지 않도록 결합
            if not url.endswith(path):
                url = url.rstrip("/") + path
            
            try:
                r = session.get(url, params={"searchKeyword": "파이썬", "q": "파이썬", "vSrchText": "파이썬"}, headers=HEADERS, timeout=4, verify=False)
                length = len(r.text)
                
                # 껍데기 에러 페이지가 아닌 정상 페이지(대체로 4000바이트 초과)
                is_valid = r.status_code == 200 and length > 3000 and "찾을 수" not in r.text and "오류" not in r.text
                
                if r.status_code == 200:
                    results[name].append({
                        "url": url,
                        "status": r.status_code,
                        "len": length,
                        "is_valid": is_valid
                    })
                    if is_valid:
                        print(f"  [SUCCESS] {dom} -> {path} (Len: {length})")
            except Exception as e:
                pass

with open("probe_rectified_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n교정 및 검증 완료. 'probe_rectified_results.json' 저장됨.")
