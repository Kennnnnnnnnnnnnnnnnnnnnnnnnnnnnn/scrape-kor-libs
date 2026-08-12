import requests, urllib3, re
urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

r = requests.get("https://www.nowonlib.kr/", headers=headers, verify=False)

# script 태그 src 들 추출
js_files = re.findall(r'src="([^"]+\.js[^"]*)"', r.text)
print("JS files:", js_files)

# page html 내 api 혹은 fetch/axios/ajax 구문
apis = re.findall(r'["\'](/api/[^"\']+)["\']', r.text)
print("APIs in main page:", set(apis))
