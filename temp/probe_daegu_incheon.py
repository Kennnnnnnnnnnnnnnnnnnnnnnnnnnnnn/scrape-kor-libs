"""
대구통합도서관 및 인천미추홀도서관 메인 검색 폼 분석
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

def analyze(name, url):
    print(f"\n=== Analyze [{name}] {url} ===")
    try:
        r = session.get(url, headers=HEADERS, timeout=8, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")
        forms = soup.select("form")
        print(f"  Forms found: {len(forms)}")
        for i, f in enumerate(forms):
            print(f"    Form[{i}] action={f.get('action')} method={f.get('method')}")
            for inp in f.select("input, select"):
                print(f"      <{inp.name}> name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")
        
        for j, sc in enumerate(soup.select("script")):
            txt = sc.text
            if any(w in txt for w in ["search", "Search", "submit", "action"]):
                print(f"    Script[{j}] has search matches:")
                for line in txt.split("\n"):
                    if any(w in line for w in ["action", "submit", "href", "search"]):
                        print(f"      {line.strip()[:100]}")
    except Exception as e:
        print(f"  Error: {e}")

analyze("대구도서관 포털", "https://library.daegu.go.kr/main/index.do")
analyze("대구도서관 메인", "https://library.daegu.go.kr/kor/index.do")
analyze("인천미추홀", "https://michuhollib.incheon.go.kr/kor/index.do")
analyze("인천미추홀 메인", "https://michuhollib.incheon.go.kr/main/index.do")
