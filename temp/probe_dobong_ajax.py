import requests, urllib3, re
urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

r = requests.get("https://www.unilib.dobong.kr/nanum/ndls/common/js/bookSearch.js", headers=headers, verify=False)

matches = re.findall(r'.{0,100}getBookInfo\.do.{0,300}', r.text)
for m in matches:
    print("MATCH:", m)
    print("-" * 50)
