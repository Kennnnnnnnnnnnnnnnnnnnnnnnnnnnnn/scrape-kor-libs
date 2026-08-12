"""
광명시도서관 wdDataSearch.js 스크립트 다운로드 및 분석
"""
import requests
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
HEADERS = {'User-Agent': 'Mozilla/5.0'}

url = "https://gmlib.gm.go.kr/dls_le/wdModules/wdDataSearch/skins/default/jslib/wdDataSearch.js"

try:
    r = session.get(url, headers=HEADERS, timeout=8, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    
    with open("gwangmyeong_wdSearch.js", "w", encoding="utf-8") as f:
        f.write(r.text)
        
    # ajax, post, get, url, dataDetail 단어 주변 분석
    lines = r.text.split("\n")
    print(f"Total lines: {len(lines)}")
    matches = []
    for line in lines:
        if any(w in line for w in ["ajax", "post", "get", "url", "dataDetail", "json"]):
            matches.append(line.strip()[:150])
            
    print(f"Matches found: {len(matches)}")
    for m in matches[:25]:
        print("  ", m)
except Exception as e:
    print("Error:", e)
