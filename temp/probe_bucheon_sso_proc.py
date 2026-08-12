"""
부천시 ssoProc.jsp 연동 체인 실시간 검증
"""
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import urllib.parse
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
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
session.mount('http://', SslAdapter())
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# 1. IP 가져오기 시도
client_ip = "127.0.0.1"
try:
    r_ip = session.post("https://sso.bucheon.go.kr/sso/api/cors/get/ip", headers=HEADERS, timeout=5, verify=False)
    if r_ip.status_code == 200:
        res_json = r_ip.json()
        client_ip = res_json.get("client_ip", "127.0.0.1")
        print("Obtained IP:", client_ip)
except Exception as e:
    print("IP error, using default IP:", e)

# 2. ssoProc.jsp 호출
url_proc = "https://alpasq.bcl.go.kr/alpasq-kolas-daemon/sso/bcl/ssoProc.jsp"
payload = {
    "pni_client_ip": client_ip,
    "route": "SEARCH",
    "keyword": urllib.parse.quote("파이썬"),
    "param": ""
}

print(f"=== POST {url_proc} ===")
r_proc = session.post(url_proc, data=payload, headers=HEADERS, timeout=12, verify=False, allow_redirects=True)
print("Proc Status:", r_proc.status_code)
print("Final URL:", r_proc.url)
print("Length:", len(r_proc.text))
print("'파이썬' count:", r_proc.text.count("파이썬"))

if r_proc.status_code == 200 and len(r_proc.text) > 1000:
    with open("bucheon_sso_proc_result.html", "w", encoding="utf-8") as f:
        f.write(r_proc.text)
    print("Saved bucheon_sso_proc_result.html")

    soup = BeautifulSoup(r_proc.text, "html.parser")
    # 스크립트 및 폼 파싱
    print("Forms on final page:", len(soup.select("form")))
    for form in soup.select("form"):
        print("  Form action:", form.get("action"))

    for sc in soup.select("script"):
        txt = sc.text
        if "location" in txt or "href" in txt or "action" in txt:
            for line in txt.split("\n"):
                if any(w in line for w in ["location", "href", "action", "url"]):
                    print("  Script line:", line.strip()[:150])
