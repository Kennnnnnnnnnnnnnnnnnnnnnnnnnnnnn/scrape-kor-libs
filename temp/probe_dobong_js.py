import requests, urllib3, re
urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

r = requests.get("https://www.unilib.dobong.kr/site/search/search00.do?cmd_name=bookandnonbooksearch&search_type=detail&manage_code=MA,MB,MC,ME,MG,MJ,MF,MH,SA,MD,SB,SL,SM,SN,SO,SP,SK,SQ,SR,SS,ST,SU,SG,SH,SC&search_txt=%ED%8C%8C%EC%B9%9C%EC%BD%94", headers=headers, verify=False)

cmds = re.findall(r'cmd_name=([a-zA-Z0-9_]+)', r.text)
print("cmd_name found in HTML:", set(cmds))

# js 파일 링크들 탐색
js_links = re.findall(r'src="([^"]+\.js[^"]*)"', r.text)
print("JS Links:", js_links)
