"""
미구현된 모든 도서관들의 검색 URL 패턴 전수 조사 스크립트
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
_SSL_CIPHERS = 'DEFAULT@SECLEVEL=0'

class SslAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context(ciphers=_SSL_CIPHERS)
        ctx.check_hostname = False
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

# 검증할 URL 패턴 유형들
PATTERNS = {
    "jnet_A": "/intro/menu/10003/program/30001/searchResultList.do",
    "jnet_B": "/intro/menu/10181/program/30012/plusSearchResultList.do",
    "kolas_A": "/search/searchDetail.do",
    "kolas_B": "/search/tot/result.do",
    "slima_A": "/search/search_detail.do",
    "slima_B": "/search/search.do",
}

# 남은 도서관들과 도메인 매핑
# 사용자가 제공한 텍스트에서 도메인을 추출하여 딕셔너리로 구축
DOMAIN_MAP = {
    # 경기도
    "수원시": "suwonlib.go.kr",
    "부천시": "bcl.go.kr",
    "안산시": "lib.ansan.go.kr",
    "의정부시": "uabl.go.kr",
    "파주시": "lib.paju.go.kr",
    "시흥시": "lib.siheung.go.kr",
    "김포시": "lib.gimpo.go.kr",
    "광명시": "gmlib.gm.go.kr",
    "광주시": "lib.gjcity.go.kr",
    "군포시": "gunpolib.go.kr",
    "하남시": "lib.hanam.go.kr",
    "양주시": "lib.yangju.go.kr",
    "이천시": "icheonlib.go.kr",
    "안성시": "ansengl.go.kr",
    "의왕시": "uwlib.go.kr",
    "여주시": "yjlib.go.kr",
    "동두천시": "lib.ddc.go.kr",
    "가평군": "gplib.go.kr",
    "연천군": "library.yeoncheon.go.kr",
    # 서울
    "서울도서관": "lib.seoul.go.kr",
    "서울시교육청도서관": "lib.sen.go.kr",
    "강동구립도서관": "gdlibrary.or.kr",
    "강북구립도서관": "gblib.or.kr",
    "관악구립도서관": "gwanaklib.seoul.kr",
    "광진구립도서관": "gjl.or.kr",
    "구로구립도서관": "lib.guro.go.kr",
    "금천구립도서관": "geumcheonlib.seoul.kr",
    "노원구립도서관": "nowonlib.kr",
    "도봉구립도서관": "unilib.dobong.go.kr",
    "동대문구립도서관": "l4u.dongdeamun.go.kr",
    "동작구립도서관": "dongjaklib.or.kr",
    "마포구립도서관": "mapolib.or.kr",
    "서대문구립도서관": "sdmlib.or.kr",
    "서초구립도서관": "seocholib.or.kr",
    "성동구립도서관": "sdlib.or.kr",
    "성북구립도서관": "sblib.seoul.kr",
    "양천구립도서관": "yangcheonlib.or.kr",
    "영등포구립도서관": "ydplib.or.kr",
    "용산구립도서관": "yslibrary.or.kr",
    "은평구립도서관": "eplib.or.kr",
    "종로구립도서관": "lib.jongno.go.kr",
    "중구립도서관": "e-book.e-junggu.or.kr",
    "중랑구립도서관": "junglanglib.seoul.kr",
    # 부산
    "부산광역시립시민도서관": "siminlib.go.kr",
    "해운대구립도서관": "haeundae.go.kr/library",
    "금정구립도서관": "geumjeong.go.kr/library",
    "사하구립도서관": "saha.go.kr/library",
    # 대구
    "대구광역시립도서관통합포털": "library.daegu.go.kr",
    "수성구립도서관": "suseonglib.or.kr",
    "달서구립도서관": "dalseolib.daegu.kr",
    # 인천
    "미추홀도서관": "michuhollib.incheon.go.kr",
    "인천광역시교육청도서관": "ijlib.or.kr",
    "부평구립도서관": "bppl.or.kr",
    "연수구립도서관": "yslib.go.kr",
    # 광주
    "광주광역시립도서관": "citylib.gwangju.kr",
    "광산구립도서관": "lib.gwangsan.go.kr",
    "남구립도서관": "lib.namgu.gwangju.kr",
    # 대전
    "한밭도서관": "hanbatlib.daejeon.go.kr",
    "서구립도서관": "geolib.or.kr",  # seogu.go.kr/learning/gasuwonlib 대체 확인 필요
    "유성구립도서관": "yuseong.go.kr/lib",
    # 울산
    "울산도서관": "library.ulsan.go.kr",
    "북구립도서관": "usbl.bukgu.ulsan.kr",
    "울주군립도서관": "uljulib.or.kr",
    # 세종
    "세종특별자치시립도서관": "lib.sejong.go.kr",
    # 강원
    "강원특별자치도교육청도서관": "lib.gwe.go.kr",
    "춘천시립도서관": "citylib.chuncheon.go.kr",
    "강릉시립도서관": "gnslib.or.kr",
    "원주시립도서관": "lib.wonju.go.kr",
    # 충북
    "청주시립도서관": "library.cheongju.go.kr",
    "충주시립도서관": "lib.chungju.go.kr",
    "제천시립도서관": "jecheon.go.kr/site/lib",
    # 충남
    "충청남도도서관": "library.cn.go.kr",
    "천안시도서관": "naru.cheonan.go.kr",
    "아산시립도서관": "ascl.asan.go.kr",
    "논산시립도서관": "lib.nonsan.go.kr",
    # 전북
    "전북도서관": "library.jeonbuk.go.kr",
    "전주시립도서관": "lib.jeonju.go.kr",
    "군산시립도서관": "lib.gunsan.go.kr",
    "익산시립도서관": "lib.iksan.go.kr",
    # 전남
    "전라남도립도서관": "lib.jeonnam.go.kr",
    "목포시립도서관": "mokpolib.or.kr",
    "여수시립도서관": "yslib.yeosu.go.kr",
    "순천시립도서관": "library.suncheon.go.kr",
    # 경북
    "경상북도교육청대표도서관": "gbelib.kr",
    "포항시립도서관": "phlib.pohang.go.kr",
    "구미시립도서관": "lib.gumi.go.kr",
    "경주시립도서관": "gjl.gyeongju.go.kr",
    # 경남
    "경상남도대표도서관": "gnlib.or.kr",
    "창원시립도서관": "cwlib.changwon.go.kr",
    "김해시립도서관": "lib.gimhae.go.kr",
    "진주시립도서관": "lib.jinju.go.kr",
}

session = requests.Session()
session.mount('https://', SslAdapter())

results = {}

print("전수 조사 시작...")
for name, domain in DOMAIN_MAP.items():
    results[name] = {"domain": domain, "working_pattern": None, "details": {}}
    for p_name, path in PATTERNS.items():
        url = f"https://{domain}{path}"
        try:
            r = session.get(url, params={"searchKeyword": "파이썬", "q": "파이썬"}, headers=HEADERS, timeout=5, verify=False)
            status = r.status_code
            length = len(r.text)
            has_cnt = "totalCnt" in r.text or "totalCount" in r.text or "total" in r.text.lower()
            
            results[name]["details"][p_name] = {"status": status, "len": length, "has_cnt": has_cnt}
            
            if status == 200 and length > 3000:
                results[name]["working_pattern"] = p_name
                print(f"[SUCCESS] {name} ({domain}) -> {p_name} (len: {length})")
                break
        except Exception as e:
            results[name]["details"][p_name] = {"error": str(e)}
    
    if not results[name]["working_pattern"]:
        print(f"[FAILED] {name} ({domain})")

with open("probe_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n전수 조사 완료. 'probe_results.json' 저장됨.")
