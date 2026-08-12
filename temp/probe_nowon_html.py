import requests, urllib3, re
urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

r = requests.get("https://www.nowonlib.kr/intro/menu/10003/program/30001/searchResultList.do?searchType=SIMPLE&searchKeyword=%ED%8C%8C%EC%B9%9C%EC%BD%94", headers=headers, verify=False)

print("Status:", r.status_code)
# api 엔드포인트 관련 문자열 찾기
matches = re.findall(r'/api/[a-zA-Z0-9_/]+', r.text)
print("API endpoints found in HTML:", set(matches))

# plusSearchResultList.do 인지 확인
print("plusSearchResultList in text:", "plusSearchResultList" in r.text)
print("searchResultList in text:", "searchResultList" in r.text)
