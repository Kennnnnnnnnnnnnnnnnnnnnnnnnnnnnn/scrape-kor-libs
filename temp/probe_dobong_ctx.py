import requests, urllib3
urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

r = requests.get("https://www.unilib.dobong.kr/nanum/ndls/common/js/bookSearch.js", headers=headers, verify=False)

idx = r.text.find('/ndls/bookSearch/getBookInfo.do"')
print(r.text[idx-200:idx+500])
