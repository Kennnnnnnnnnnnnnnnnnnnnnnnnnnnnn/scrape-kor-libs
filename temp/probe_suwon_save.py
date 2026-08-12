"""
수원시 도서관 응답 HTML 바디 UTF-8 파일 저장
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

_SSL_CIPHERS = 'DEFAULT@SECLEVEL=0'
class SslAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        ctx = create_urllib3_context(ciphers=_SSL_CIPHERS)
        ctx.check_hostname = False
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

s = requests.Session()
s.mount('https://', SslAdapter())

try:
    r = s.get('https://www.suwonlib.go.kr/search/searchDetail.do', headers={'User-Agent':'Mozilla/5.0'}, verify=False, timeout=10)
    with open("suwon_resp.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    print("Saved suwon_resp.html. Length:", len(r.text))
except Exception as e:
    print("Error:", e)
