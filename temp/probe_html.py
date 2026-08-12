"""
jnet 기반 도서관 사이트 HTML 구조 상세 분석 스크립트
searchResultList.do (Type A)와 plusSearchResultList.do (Type B) 파싱 검증
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
_SSL_CIPHERS = 'DEFAULT@SECLEVEL=0'

class SslAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context(ciphers=_SSL_CIPHERS)
        ctx.check_hostname = False
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)


def analyze_type_a(domain, kw="파이썬"):
    """Type A: searchResultList.do (화성/안양/고양/구리/과천 패턴)"""
    url = f"https://{domain}/intro/menu/10003/program/30001/searchResultList.do"
    params = {"searchType": "SIMPLE", "searchKeyword": kw}
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        
        total_tag = soup.select_one("#totalCnt")
        total = total_tag.text.strip() if total_tag else "N/A"
        
        book_items = soup.select("#bookList > div:nth-of-type(1) > ul:nth-of-type(1) > li")
        print(f"  [Type A] totalCnt={total}, bookItems={len(book_items)}")
        
        if book_items:
            item = book_items[0]
            path_data = "div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1)"
            title_tag = item.select_one(f"{path_data} > p > a")
            if title_tag:
                print(f"    Title: {title_tag.get('title', title_tag.text.strip())[:60]}")
            
            info_lis = item.select(f"{path_data} > ul > li")
            for i, li in enumerate(info_lis):
                spans = li.select("span")
                span_texts = [s.text.strip()[:40] for s in spans]
                print(f"    li[{i}] spans: {span_texts}")
    except Exception as e:
        print(f"  [Type A] ERROR: {e}")


def analyze_type_b(domain, kw="파이썬"):
    """Type B: plusSearchResultList.do (용인/성남/남양주/강남/송파 패턴)"""
    url = f"https://{domain}/intro/menu/10181/program/30012/plusSearchResultList.do"
    params = {"searchType": "SIMPLE", "searchCategory": "BOOK", "searchKey": "TITLE", "searchKeyword": kw, "searchOrder": "DESC"}
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        
        # 총 건수 - 다양한 셀렉터 시도
        total_tags = soup.select("strong.highlight")
        if total_tags:
            print(f"  [Type B] highlight strongs: {[t.text.strip() for t in total_tags[:5]]}")
        
        # 도서 목록 - 다양한 셀렉터 시도
        selectors = [
            "#searchForm > div > div:nth-of-type(3) > div:nth-of-type(2) > ul > li",
            "ul.resultList > li",
            ".search-result-list > li",
            "div.bookArea > ul > li",
            ".bookList > li",
        ]
        for sel in selectors:
            items = soup.select(sel)
            if items:
                print(f"  [Type B] selector='{sel}', count={len(items)}")
                item = items[0]
                # 제목, 저자, 청구기호 구조 분석
                all_a = item.select("a")
                for a in all_a[:3]:
                    print(f"    <a>: {a.text.strip()[:60]}")
                all_p = item.select("p")
                for p in all_p[:5]:
                    print(f"    <p>: {p.text.strip()[:60]}")
                all_div = item.select("div")
                for d in all_div[:5]:
                    if d.text.strip() and len(d.text.strip()) < 100:
                        print(f"    <div>: {d.text.strip()[:80]}")
                break
        else:
            # 더 일반적인 탐색
            all_lis = soup.select("li")
            book_lis = [li for li in all_lis if li.select_one("a") and len(li.text) > 50]
            print(f"  [Type B] generic li with <a> (>50 chars): {len(book_lis)}")
            if book_lis:
                print(f"    First: {book_lis[0].text.strip()[:200]}")
    except Exception as e:
        print(f"  [Type B] ERROR: {e}")


# ---- Type A 사이트 분석 ----
print("=" * 80)
print("TYPE A 사이트 (searchResultList.do) 분석")
print("=" * 80)

type_a_sites = {
    "고양시": "www.goyanglib.or.kr",
    "구리시": "www.gurilib.go.kr",
    "과천시": "www.gclib.go.kr",
}
for city, domain in type_a_sites.items():
    print(f"\n--- {city} ({domain}) ---")
    analyze_type_a(domain)


# ---- Type B 사이트 분석 ----
print("\n" + "=" * 80)
print("TYPE B 사이트 (plusSearchResultList.do) 분석")
print("=" * 80)

type_b_sites = {
    "성남시": "www.snlib.go.kr",
    "남양주시": "lib.nyj.go.kr",
    "평택시": "www.ptlib.go.kr",
    "오산시": "www.osanlibrary.go.kr",
    "포천시": "lib.pocheon.go.kr",
    "강남구립": "library.gangnam.go.kr",
    "송파구립": "www.splib.or.kr",
}
for city, domain in type_b_sites.items():
    print(f"\n--- {city} ({domain}) ---")
    analyze_type_b(domain)
