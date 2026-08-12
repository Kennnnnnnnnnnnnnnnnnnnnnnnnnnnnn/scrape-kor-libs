"""
안양시립도서관 공용 스크립트 다운로드 및 fnCollectionInfo 탐색
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
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

base_url = "https://lib.anyang.go.kr"
files = [
    "/include/js/common.js",
    "/include/booksearch/js/ui.js",
    "/include/booksearch/js/alpasq.js"
]

for f in files:
    url = base_url + f
    try:
        r = session.get(url, headers=HEADERS, timeout=8, verify=False)
        print(f"Downloaded: {f} -> Status: {r.status_code}, Length: {len(r.text)}")
        out_name = "anyang_" + f.split("/")[-1]
        with open(out_name, "w", encoding="utf-8") as out:
            out.write(r.text)
            
        # fnCollectionInfo 단어 검색
        if "fnCollectionInfo" in r.text:
            print(f"  [FOUND fnCollectionInfo in {out_name}!!!]")
            idx = r.text.find("fnCollectionInfo")
            print("  Snippet:", r.text[idx:idx+450].replace("\n", " "))
    except Exception as e:
        print("Error:", e)
