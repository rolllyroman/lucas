#coding:utf-8
import requests
import time
from lxml import etree
import json

import pymysql
import random

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chromeOptions = webdriver.ChromeOptions()

class Spider(object):


    def __init__(self):
        # 代理池
        self.op_proxies = []  

        # 西刺url
        self.ip_url = "https://www.xicidaili.com/nn/%s"
        # 西刺第几页
        self.nn = 0

    def get_ip(self):
        if not self.op_proxies:
            self.nn += 1
            resp = requests.get(self.ip_url%self.nn)
            content = resp.content

            html = etree.HTML(content)


            xieyi_list = html.xpath("//tr/td[last()-4]/text()")
            port_list = html.xpath("//tr/td[last()-7]/text()")
            ip_list = html.xpath("//tr/td[last()-8]/text()")

            for i,ip in enumerate(ip_list):
                port = port_list[i]
                xieyi = xieyi_list[i].lower()

                op_proxy = "--proxy-server=%s//%s:%s"%(xieyi,ip,port)

                self.op_proxies.append(op_proxy)




# 设置代理
chromeOptions.add_argument("--proxy-server=http://112.85.167.11:9999")
# 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
driver = webdriver.Chrome(chrome_options = chromeOptions)

BASIC_URL = "https://weixin.sogou.com/weixin?query=%s&_sug_type_=&s_from=input&_sug_=n&type=1&page=%s&ie=utf8"

conn = pymysql.connect(host="119.23.52.3",user="root",passwd="168mysql",db="haha",charset="utf8")  
conn.autocommit(1) # conn.autocommit(True) 
cursor = conn.cursor()



def search_list(word):
    print "search_list:%s"%word
    for i in range(1,11):
        url = BASIC_URL%(word,i)
        # resp = requests.get(url,headers=HEADERS)
        driver.get(url)

        time.sleep(1)

        content = driver.page_source.encode("utf-8")
        html = etree.HTML(content)


        weixins = html.xpath("//label/text()")
        detail_srcs = html.xpath("//li//div/p[@class='tit']/a/@href")

        weixins,detail_srcs = if_list_code(weixins,detail_srcs)

        if not weixins:
            break

        deal_detail(weixins,detail_srcs)

def get_words():
    words = set()
    url = "https://hanyu.baidu.com/s?wd=%E7%99%BE%E5%AE%B6%E5%A7%93&from=poem"
    resp = requests.get(url,headers=HEADERS)

    resp.encoding = "utf-8"
    html = resp.text

    for w in html:
        words.add(w)
    return words

def main():
    print "main start..."
    words = get_words()
    for w in words:
        sql = "select word from got_word where word = %s"
        cursor.execute(sql,(w,))
        if cursor.fetchone():
            print "%s 已搜过，跳过..."%w
            continue

        print "开始搜索:%s"%w
        search_list(w)

        sql = "insert into got_word(word) values(%s)"
        cursor.execute(sql,(w,))

def deal_detail(weixins,detail_srcs):
    print "deal_detail start..."

    for i,weixin in enumerate(weixins):    
        sql = "select weixin from robot where weixin = %s"
        cursor.execute(sql,(weixin,))
        res = cursor.fetchone()
        if res:
            continue

        src = detail_srcs[i]

        # 详情名字和头像
        # resp = requests.get(src,headers=HEADERS)
        # html = etree.HTML(resp.content)

        driver.get(src)
        content = driver.page_source.encode("utf-8")
        html = etree.HTML(content)

        heads = html.xpath("//div//span/img/@src")
        names = html.xpath("//strong/text()")

        heads,names = if_detail_code(heads,names)

        head = heads[0].replace("http","https")
        name = names[0].strip()

        sql = "insert into robot(weixin,name,head) values(%s,%s,%s)"
        cursor.execute(sql,(weixin,name,head))

        print weixin,name,head,"ok!" 
        time.sleep(1)


if __name__ == "__main__":
    main()
    cursor.close()
    conn.close()
    driver.close()
