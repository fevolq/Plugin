#!-*- coding:utf-8 -*-
# FileName: 谷歌登录（获取登录后的跳转链接）
# pip install DrissionPage==4.0.5.6

import traceback
from urllib.parse import unquote

from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions
from DrissionPage.errors import *

import config
from utils import log_sls


class Chrome:

    def __init__(self):
        self.max_retry = 3  # 只有捕获的指定异常才重试
        self._option = ChromiumOptions()
        self._option.set_browser_path(path=config.CHROME_PATH)
        self.__set_argument()

        self.driver = ChromiumPage(self._option)

    def __set_argument(self):
        self._option.headless()  # 无头模式
        self._option.set_user_agent(  # 必须设置UA，否则无头模式下会触发反爬，导致拒绝
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')
        self._option.set_argument('--no-sandbox')  #
        self._option.set_argument("--incognito")  # 匿名模式
        self._option.set_argument("--disable-gpu")
        self._option.set_argument("--disable-popup-blocking")
        self._option.set_argument("--profile-directory=Default")
        self._option.set_argument("--ignore-certificate-errors")
        self._option.set_argument("--disable-plugins-discovery")
        self._option.set_argument('--no-first-run')
        self._option.set_argument('--no-service-autorun')
        self._option.set_argument('--no-default-browser-check')
        self._option.set_argument('--password-store=basic')
        self._option.set_argument('--disable-blink-features=AutomationControlled')
        self._option.set_argument('--disable-dev-shm-usage')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.driver.close()
            self.driver.quit()
            self.driver = None
        except:
            pass

    def google_login(self, url, *, email, password, retry=1) -> (str, bool):
        res, success = '', True
        try:
            if retry > self.max_retry:
                raise Exception(f'达到最大重试次数：{self.max_retry}')
            self.driver.get(url)

            self.driver.ele('#identifierId').input(email)
            self.driver.ele('#identifierNext').click()

            self.driver.wait.url_change('challenge')  # 等待链接改变
            current_url = self.driver.url
            if current_url.find('recaptcha') >= 0:
                raise Exception('触发程序识别')
            elif current_url.find('pwd') < 0:
                raise Exception('未到达密码页面')

            self.driver.wait.doc_loaded()  # 等待页面加载完成
            self.driver.ele('@name=Passwd').input(password)
            self.driver.ele('#passwordNext').click()

            self.driver.wait.url_change('accounts/SetSID')
            self.driver.wait.url_change('scope')  # 等待跳转到最终的链接
            res = unquote(self.driver.url)
        except PageDisconnectedError:
            return self.google_login(url, email=email, password=password, retry=retry + 1)
        except Exception as e:
            success = False
            res = str(e)
            log_sls.error('chrome', '登录异常',
                          error=traceback.format_exc(), e=str(e),
                          retry=retry,
                          )

        return res, success

    def get_html(self, url) -> (str, bool):
        res, success = '', True
        try:
            self.driver.get(url)
            res = self.driver.html
        except Exception as e:
            success = False
            res = str(e)

        return res, success
