import requests, urllib3, json
urllib3.disable_warnings()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

url = "https://www.unilib.dobong.kr/ndls/bookSearch/getBookInfo.do"
params = {
    "manage_code": "SG",
    "reckey": "247635471",
    "species_key": "247635468"
}

r = requests.get(url, params=params, headers=headers, verify=False)
print("Dobong getBookInfo Status:", r.status_code)
print(r.text[:1500])

# 성동
url_sd = "https://www.sdlib.or.kr/SD/ndls/bookSearch/getBookInfo.do"
params_sd = {
    "manage_code": "MA",
    "reckey": "217164322",
    "species_key": "217164321"
}
r_sd = requests.get(url_sd, params=params_sd, headers=headers, verify=False)
print("\nSeongdong getBookInfo Status:", r_sd.status_code)
print(r_sd.text[:1500])
