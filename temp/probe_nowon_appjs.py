import requests, urllib3, re
urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://www.nowonlib.kr/app.b3db5ae29841db0aac18.js"
r = requests.get(url, headers=headers, verify=False)
print("JS Size:", len(r.text))

apis = re.findall(r'/api/[a-zA-Z0-9_/]+', r.text)
print("Unique APIs in app.js:", sorted(set(apis)))
