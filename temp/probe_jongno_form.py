import requests, urllib3, re
urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

r = requests.get("https://lib.jongno.go.kr/", headers=headers, verify=False)

forms = re.findall(r'<form[^>]+action="([^"]+)"', r.text)
print("Forms in jongno main page:", forms)
