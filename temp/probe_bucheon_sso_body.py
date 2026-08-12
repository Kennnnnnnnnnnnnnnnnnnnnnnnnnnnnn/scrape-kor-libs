"""
부천시 ssoProc.jsp 응답 본문 분석
"""
import requests
import urllib.parse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

session = requests.Session()
HEADERS = {'User-Agent': 'Mozilla/5.0'}
proc_url = "https://alpasq.bcl.go.kr/alpasq-kolas-daemon/sso/bcl/ssoProc.jsp"
payload = {
    "pni_client_ip": "127.0.0.1",
    "route": "SEARCH",
    "keyword": urllib.parse.quote("파이썬"),
    "param": ""
}

try:
    r = session.post(proc_url, data=payload, headers=HEADERS, timeout=8, verify=False)
    print("Length:", len(r.text))
    print(r.text)
except Exception as e:
    print(e)
