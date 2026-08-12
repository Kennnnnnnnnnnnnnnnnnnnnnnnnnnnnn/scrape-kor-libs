import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
try:
    r = requests.get('https://sso.bucheon.go.kr/sso/api/cors/get/ip', verify=False, timeout=8)
    print("Status:", r.status_code)
    print("Resp:", r.text)
except Exception as e:
    print("Error:", e)
