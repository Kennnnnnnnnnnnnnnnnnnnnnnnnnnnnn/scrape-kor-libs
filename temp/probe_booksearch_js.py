import requests, urllib3, re
urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

r = requests.get("https://www.unilib.dobong.kr/nanum/ndls/common/js/bookSearch.js", headers=headers, verify=False)

print("Size of bookSearch.js:", len(r.text))

cmds = re.findall(r'cmd_name[=:]\s*["\']?([a-zA-Z0-9_]+)', r.text)
print("cmd_names in bookSearch.js:", set(cmds))

# url 들 추출
urls = re.findall(r'["\']([^"\']+\.do[^"\']*)["\']', r.text)
print("URLs in bookSearch.js:", set(urls))
