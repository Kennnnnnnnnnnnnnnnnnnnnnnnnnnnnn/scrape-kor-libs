"""
시흥시 Pyxis API 지점(branches) 목록 획득 진단
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import urllib3
import json

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
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://lib.siheung.go.kr/',
    'X-Requested-With': 'XMLHttpRequest'
}

url = "https://lib.siheung.go.kr/pyxis-api/1/branches"

try:
    r = session.get(url, headers=HEADERS, timeout=8, verify=False)
    print("Status:", r.status_code)
    print("Length:", len(r.text))
    data = r.json()
    print("Success:", data.get("success"))
    if data.get("success"):
        branches = data.get("data", {}).get("list", []) or data.get("data", [])
        print(f"Branches count: {len(branches)}")
        for b in branches[:10]:
            print(f"  Branch ID: {b.get('id')}, Name: {b.get('name')}")
except Exception as e:
    print("Error:", e)
