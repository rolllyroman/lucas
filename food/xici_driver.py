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


class Spider(object):

    headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
           'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
           'Connection':'Keep-Alive',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}

    basic_url = "https://weixin.sogou.com/weixin?query=%s&_sug_type_=&s_from=input&_sug_=n&type=1&page=%s&ie=utf8"

    def __init__(self):
        # 代理池
        self.op_proxies = []  

        # 西刺url
        self.ip_url = "https://www.xicidaili.com/nt/%s"
        # 西刺第几页
        self.nn = 1

        self.driver = None

        # mysql
        self.conn = pymysql.connect(host="119.23.52.3",user="root",passwd="168mysql",db="haha",charset="utf8")  
        self.conn.autocommit(1) # conn.autocommit(True) 
        self.cursor = self.conn.cursor()

        self.words = self.get_words()


        self.list_page = 1

    def get_ip(self):
        if not self.op_proxies:
            self.nn += 1
            url = self.ip_url%self.nn

            resp = requests.get(url,headers=self.headers)
            content = resp.content

            html = etree.HTML(content)

            xieyi_list = html.xpath("//tr/td[last()-4]/text()")
            port_list = html.xpath("//tr/td[last()-7]/text()")
            ip_list = html.xpath("//tr/td[last()-8]/text()")

            for i,ip in enumerate(ip_list):
                port = port_list[i]
                xieyi = xieyi_list[i].lower()

                op_proxy = "--proxy-server=%s://%s:%s"%(xieyi,ip,port)

                self.op_proxies.append(op_proxy)

            print "ip池更新：%s"%self.op_proxies

        return self.op_proxies.pop()

    def get_words(self):
        words = set()
        url = "https://hanyu.baidu.com/s?wd=%E7%99%BE%E5%AE%B6%E5%A7%93&from=poem"
        resp = requests.get(url,headers=self.headers)

        resp.encoding = "utf-8"
        html = resp.text

        for w in html:
            words.add(w)
        return words

    def start_search(self):
        for w in self.words:
            sql = "select word from got_word where word = %s"
            self.cursor.execute(sql,(w,))
            if self.cursor.fetchone():
                print "%s 已搜过，跳过..."%w
                continue

            print "开始搜索:%s"%w
            self.search_list(w)

            time.sleep(1)

            self.list_page = 1
            print "%s 爬取完毕，列表页重新从%s开始爬取"%(w,self.list_page)


            sql = "delete from got_word where num = 0"
            self.cursor.execute(sql)
            sql = "insert into got_word(word) values(%s)"
            self.cursor.execute(sql,(w,))

    def run(self):
        chromeOptions = webdriver.ChromeOptions()
        # 设置代理
        self.ip = self.get_ip()
        chromeOptions.add_argument(self.ip)

        # 把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
        # chromeOptions.set_headless()

        # 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
        self.driver = webdriver.Chrome(chrome_options = chromeOptions)

        # 测试ip是否可以用
        print "ip:%s"%self.ip
        # try:

        # test_url = "http://httpbin.org/ip"
        # self.driver.get(test_url)
        # test_source = self.driver.page_source
        # if len(test_source)>200:
        #     print "测试ip失败，ip不可用，跳过...".decode('utf-8').encode('gb2312')
        #     self.driver.quit()
        #     self.run()

        # except:
        #     print "超时,开始更换ip爬取...".decode('utf-8').encode('gb2312')
        #     self.driver.close()
        #     self.run()
        

        self.start_search()

    def search_list(self,word):
        while self.list_page < 11:
            print "开始爬取 %s 列表页第%s页..."%(word,self.list_page)
            url = self.basic_url%(word,self.list_page)
            # resp = requests.get(url,headers=HEADERS)
            try:
                self.driver.get(url)
            except:
                print "超时,开始更换ip爬取..."
                self.driver.close()
                time.sleep(1)
                self.run()

            time.sleep(1)

            content = self.driver.page_source.encode("utf-8")
            html = etree.HTML(content)

            weixins = html.xpath("//label/text()")
            detail_srcs = html.xpath("//li//div/p[@class='tit']/a/@href")

            if len(weixins) == 1:
                print "错误:%s,开始更换ip爬取..."%weixins[0]
                self.driver.close()
                time.sleep(1)
                self.run()

            if not weixins:
                break

            self.deal_detail(weixins,detail_srcs,word)

            self.list_page += 1


    def deal_detail(self,weixins,detail_srcs,word):

        for i,weixin in enumerate(weixins):    
            sql = "select weixin from robot where weixin = %s"
            self.cursor.execute(sql,(weixin,))
            res = self.cursor.fetchone()
            if res:
                continue

            print "准备进入详情页，开始获取头像和姓名..."
            src = detail_srcs[i]

            try:
                self.driver.get(src)
            except:
                print "超时,开始更换ip爬取..."
                self.driver.close()
                time.sleep(1)
                self.run()

            content = self.driver.page_source.encode("utf-8")
            html = etree.HTML(content)

            heads = html.xpath("//div//span/img/@src")
            names = html.xpath("//strong/text()")

            if not names:
                print "ip被判断为非正常用户，开始更换ip爬取..."
                self.driver.close()
                time.sleep(1)
                self.run()

            head = heads[0].replace("http","https")
            name = names[0].strip()

            sql = "insert into robot(weixin,name,head) values(%s,%s,%s)"
            self.cursor.execute(sql,(weixin,name,head))

            sql = "update got_word set num = num + 1 where word = %s"
            self.cursor.execute(sql,(word,))

            print weixin,name,head,"ok!" 
            time.sleep(1)

    def __del__(self):
        self.cursor.close()
        self.conn.close()
        self.driver.close()

if __name__ == "__main__":
    Spider().run()
