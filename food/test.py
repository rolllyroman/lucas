#coding:utf-8
import requests
import time
from lxml import etree
import json

# import MySQLdb
import pymysql
import random

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

# from selenium import webdriver
# chromeOptions = webdriver.ChromeOptions()

# # 设置代理
# # 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
# browser = webdriver.Chrome(chrome_options = chromeOptions)

# # 查看本机ip，查看代理是否起作用
# browser.get("http://httpbin.org/ip")
# s1 = browser.page_source

# # 退出，清除浏览器缓存
# browser.quit()

# chromeOptions.add_argument("--proxy-server=http://14.115.106.218:808")
# browser = webdriver.Chrome(chrome_options = chromeOptions)
# browser.get("http://httpbin.org/ip")
# s2 = browser.page_source

# browser.quit()

proxies = {"http":"http://14.115.106.218:808","https":"https://125.123.139.172:9000"}
proxies = {"http":"http://14.115.106.218:808"}
proxies = {"https":"https://125.123.139.172:9000"}
url = "https://weixin.sogou.com/weixin?query=1&_sug_type_=&s_from=input&_sug_=n&type=1&page=1&ie=utf8"
resp = requests.get(url,proxies=proxies)

print resp.apparent_encoding
print requests.utils.get_encodings_from_content(resp.text)
resp.encoding = "utf-8"
print resp.text.encode("GBK",'ignore')