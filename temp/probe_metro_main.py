"""
광역 단위 주요 도서관 메인페이지 검색 폼/스크립트 일괄 분석
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3

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

METRO_DOMAINS = {
    "대구광역시": "library.daegu.go.kr",
    "대전한밭": "hanbatlib.daejeon.go.kr",
    "울산도서관": "library.ulsan.go.kr",
    "세종특별자치시": "lib.sejong.go.kr",
    "전북도서관": "library.jeonbuk.go.kr",
    "전남립도서관": "lib.jeonnam.go.kr",
    "경북도서관": "gbelib.kr",
    "경남도서관": "gnlib.or.kr"
}

results = {}

for name, domain in METRO_DOMAINS.items():
    print(f"\n=== Analyze [{name}] {domain} ===")
    url = f"https://{domain}"
    try:
        r = session.get(url, headers=HEADERS, timeout=8, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        
        forms = soup.select("form")
        print(f"  Forms found: {len(forms)}")
        for i, f in enumerate(forms):
            print(f"    Form[{i}] action={f.get('action')} method={f.get('method')}")
            for inp in f.select("input, select"):
                print(f"      <{inp.name}> name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")
        
        # 스크립트 검색어 매칭
        for j, sc in enumerate(soup.select("script")):
            txt = sc.text
            if any(w in txt for w in ["search", "Search", "submit", "action"]):
                print(f"    Script[{j}] has search matches:")
                for line in txt.split("\n"):
                    if any(w in line for w in ["action", "submit", "href", "search"]):
                        print(f"      {line.strip()[:100]}")
    except Exception as e:
        print(f"  Error: {e}")
