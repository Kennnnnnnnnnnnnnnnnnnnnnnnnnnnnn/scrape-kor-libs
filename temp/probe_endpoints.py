"""
광범위한 도서관 사이트 엔드포인트 조사 스크립트 (확장)
- jnet 패턴 외에 다양한 URL 패턴을 시도
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# SSL 보안 수준 낮춤 (안양 등 구형 사이트)
_SSL_CIPHERS = 'DEFAULT@SECLEVEL=0'

class SslAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context(ciphers=_SSL_CIPHERS)
        ctx.check_hostname = False
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

def try_url(domain, path, kw="파이썬", use_ssl_adapter=False):
    url = f"https://{domain}{path}"
    params = {"searchType": "SIMPLE", "searchKeyword": kw}
    try:
        if use_ssl_adapter:
            s = requests.Session()
            s.mount('https://', SslAdapter())
            r = s.get(url, params=params, headers=HEADERS, timeout=8, verify=False)
            s.close()
        else:
            r = requests.get(url, params=params, headers=HEADERS, timeout=8)
        has_total = "totalCnt" in r.text
        has_booklist = "bookList" in r.text
        has_searchform = "searchForm" in r.text
        return r.status_code, len(r.text), has_total, has_booklist, has_searchform
    except Exception as e:
        return -1, 0, False, False, False

# jnet CMS 표준 검색 URL 패턴 후보들
JNET_PATTERNS = [
    "/intro/menu/10003/program/30001/searchResultList.do",
    "/intro/menu/10017/program/30001/searchResultList.do",
    "/intro/menu/10181/program/30012/plusSearchResultList.do",
]

# 조사 대상 도서관 사이트
SITES = {
    # === 경기도 ===
    "수원시": "www.suwonlib.go.kr",
    "성남시": "www.snlib.go.kr",
    "고양시": "www.goyanglib.or.kr",
    "부천시": "www.bcl.go.kr",
    "안산시": "lib.ansan.go.kr",
    "남양주시": "lib.nyj.go.kr",
    "평택시": "www.ptlib.go.kr",
    "의정부시": "www.uabl.go.kr",
    "파주시": "www.lib.paju.go.kr",
    "시흥시": "lib.siheung.go.kr",
    "김포시": "www.gimpo.go.kr",
    "광명시": "gmlib.gm.go.kr",
    "광주시": "lib.gjcity.go.kr",
    "군포시": "www.gunpolib.go.kr",
    "하남시": "www.lib.hanam.go.kr",
    "오산시": "www.osanlibrary.go.kr",
    "양주시": "lib.yangju.go.kr",
    "이천시": "www.icheonlib.go.kr",
    "구리시": "www.gurilib.go.kr",
    "안성시": "www.ansengl.go.kr",
    "포천시": "lib.pocheon.go.kr",
    "의왕시": "www.uwlib.go.kr",
    "양평군": "www.yplib.go.kr",
    "여주시": "www.yjlib.go.kr",
    "동두천시": "lib.ddc.go.kr",
    "가평군": "www.gplib.go.kr",
    "과천시": "www.gclib.go.kr",
    "연천군": "library.yeoncheon.go.kr",
    # === 서울 대표 ===
    "서울도서관": "lib.seoul.go.kr",
    "강남구립": "library.gangnam.go.kr",
    "노원구립": "www.nowonlib.kr",
    "송파구립": "www.splib.or.kr",
    "마포구립": "www.mapolib.or.kr",
    # === 광역시/도 ===
    "부산시민": "siminlib.go.kr",
    "대구통합": "library.daegu.go.kr",
    "인천미추홀": "michuhollib.incheon.go.kr",
    "세종시": "lib.sejong.go.kr",
    "청주시": "library.cheongju.go.kr",
    "전주시": "lib.jeonju.go.kr",
    "창원시": "cwlib.changwon.go.kr",
}

print("=" * 120)
print(f"{'도서관':<12} {'도메인':<30} {'패턴':<50} {'상태':>5} {'길이':>8} {'tCnt':>5} {'bList':>5} {'sForm':>5}")
print("=" * 120)

for city, domain in SITES.items():
    found = False
    for pattern in JNET_PATTERNS:
        code, length, has_t, has_b, has_s = try_url(domain, pattern)
        if code == 200 and (has_b or has_s or length > 5000):
            print(f"{city:<12} {domain:<30} {pattern:<50} {code:>5} {length:>8,} {str(has_t):>5} {str(has_b):>5} {str(has_s):>5}")
            found = True
            break
    
    if not found:
        # SSL 어댑터로 재시도
        for pattern in JNET_PATTERNS:
            code, length, has_t, has_b, has_s = try_url(domain, pattern, use_ssl_adapter=True)
            if code == 200 and (has_b or has_s or length > 5000):
                print(f"{city:<12} {domain:<30} {pattern:<50} {code:>5} {length:>8,} {str(has_t):>5} {str(has_b):>5} {str(has_s):>5} [SSL-ADAPTER]")
                found = True
                break
        
        if not found:
            print(f"{city:<12} {domain:<30} {'(NOT FOUND / ALL FAILED)':<50}")
