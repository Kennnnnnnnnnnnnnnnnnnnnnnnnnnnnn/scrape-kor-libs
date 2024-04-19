import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

CIPHERS = 'DEFAULT@SECLEVEL=0'


class SslAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(SslAdapter, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        context = create_urllib3_context(ciphers=CIPHERS)
        kwargs['ssl_context'] = context
        return super(SslAdapter, self).proxy_manager_for(*args, **kwargs)


class UtilRequest:
    def __init__(self, is_ssl, need_active):
        self.need_active = need_active
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }
        self.browser = None
        if need_active:
            chrome_options = Options()
            # chrome_options.add_experimental_option("detach", True)
            # no window
            chrome_options.add_argument('headless')
            browser = webdriver.Chrome(options=chrome_options)
            new_window = browser.window_handles[0]
            browser.switch_to.window(new_window)
            # browser.maximize_window()
            self.browser = browser
        if is_ssl:
            self.session.mount('https://', SslAdapter())

    def check_response(self, status, url):
        val = status / 100
        if val == 2:
            val = 0
        else:
            print("Response code %d for %s:" % (status, url))
        return val

    def getHtmlByGet(self, url):
        str_res = ''
        try:
            # print('** GET %s' % url)
            # res = requests.get(url, verify=False)
            res = self.session.get(url, headers=self.headers)
        except TimeoutError:
            print("The following URL isn't accessible now %s" % url)
        else:
            if self.check_response(res.status_code, url) == 0:
                str_res = res.text
        return str_res

    def getHtmlByPost(self, url, payload):
        res = None
        _res = requests.post(url, headers=self.headers, json=payload)
        if self.check_response(_res.status_code, url) != 0:
            print(payload)
        else:
            res = _res.json()
        # print(res.status_code)
        return res

    def get_by_browser(self, url):
        self.browser.get(url)
        self.browser.implicitly_wait(10)
        '''
        if res.status_code / 100 != 2:
            print("Response code %d for %s:" % (res.status_code, url))
        '''

    def get_html_from_browser(self, _class_name):
        str_res = ''
        _wait = WebDriverWait(self.browser, 60)
        try:
            _wait.until(EC.presence_of_element_located((By.CLASS_NAME, _class_name)))
            # time.sleep(60)  #
        except TimeoutException:
            print("***** Timed out ******")
        else:
            str_res = self.browser.page_source

        return str_res

    def get_elems_by_get_xpath(self, url, _xpath):
        arr = self.browser.find_elements(By.XPATH, _xpath)
        return arr

    def __del__(self):
        self.session.close()
        if self.need_active:
            self.browser.quit()




