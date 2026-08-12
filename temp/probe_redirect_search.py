"""
리다이렉션 추적 안산 및 시흥 도서관 폼 분석
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
        # allow_redirects=True 를 통해 최종 이동하는 페이지의 내용을 긁어옴
        r = session.get(url, headers=HEADERS, timeout=8, verify=False, allow_redirects=True)
        print(f"  Final URL: {r.url}")
        soup = BeautifulSoup(r.text, "html.parser")
        forms = soup.select("form")
        print(f"  Forms found: {len(forms)}")
        for i, f in enumerate(forms):
            print(f"    Form[{i}] action={f.get('action')} method={f.get('method')}")
            for inp in f.select("input, select"):
                print(f"      <{inp.name}> name={inp.get('name')} value={inp.get('value')} type={inp.get('type')}")
    except Exception as e:
        print(f"  Error: {e}")

analyze("안산시도서관", "http://lib.iansan.net")
analyze("시흥시도서관", "http://lib.siheung.go.kr")
