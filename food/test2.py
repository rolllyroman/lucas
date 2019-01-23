#coding:utf-8

from constants import USER_AGENT

headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
    'Connection':'Keep-Alive',
    "User-Agent":random.choice(USER_AGENTS),
}         


import requests

session = requests.session()