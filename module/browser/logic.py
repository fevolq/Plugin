#!-*- coding:utf-8 -*-
# FileName:

from module.browser import chrome as browser


def google_login(url, *, email, password):
    with browser.Chrome() as chrome:
        res, success = chrome.google_login(url, email=email, password=password)

    resp = {'code': 200 if success else 400}
    if success:
        resp['data'] = res
    else:
        resp['msg'] = res

    return resp


def get_html(url):
    with browser.Chrome() as chrome:
        res, success = chrome.get_html(url)

    resp = {'code': 200 if success else 400}
    if success:
        resp['data'] = res
    else:
        resp['msg'] = res

    return resp
