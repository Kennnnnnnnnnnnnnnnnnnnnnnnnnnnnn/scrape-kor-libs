"""
수원시 모바일 ajax.js 및 common.js 파일 분석
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

files = ["cloudhomepage.ajax.js", "cloudhomepage.common.js"]
for f in files:
    url = f"https://mob.suwonlib.go.kr/javascript/common/{f}"
    try:
        r = s.get(url, headers={'User-Agent':'Mozilla/5.0'}, verify=False, timeout=10)
        print(f"File: {f} -> Status: {r.status_code}, Length: {len(r.text)}")
        with open(f"suwon_{f}", "w", encoding="utf-8") as out:
            out.write(r.text)
    except Exception as e:
        print(f"File: {f} -> Error: {e}")
