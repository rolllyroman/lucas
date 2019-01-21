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

from selenium import webdriver
chromeOptions = webdriver.ChromeOptions()

# 设置代理
chromeOptions.add_argument("--proxy-server=http://112.85.167.11:9999")
# 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
browser = webdriver.Chrome(chrome_options = chromeOptions)

# 查看本机ip，查看代理是否起作用
browser.get("http://httpbin.org/ip")
print(browser.page_source)

# 退出，清除浏览器缓存
browser.quit()
