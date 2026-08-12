import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
try:
    r = requests.get("https://www.gunpolib.go.kr", verify=False, timeout=8)
    print("Length:", len(r.text))
    print(r.text[:2500])
except Exception as e:
    print(e)
