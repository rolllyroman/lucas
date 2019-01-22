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


class Spider(object):

    headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
           'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
           'Connection':'Keep-Alive',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}

    basic_url = "https://weixin.sogou.com/weixin?query=%s&_sug_type_=&s_from=input&_sug_=n&type=1&page=%s&ie=utf8"

    def __init__(self):
        # 代理池
        self.proxy_list = []  

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

    def get_proxy(self):
        if not self.proxy_list:
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

                if xieyi == "https" or xieyi == "http":
                    # op_proxy = "--proxy-server=%s://%s:%s"%(xieyi,ip,port)
                    proxy = {xieyi:"%s://%s:%s"%(xieyi,ip,port)}
                    self.proxy_list.append(proxy)

            print "ip池更新：%s"%self.proxy_list

        return self.proxy_list.pop()

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

            time.sleep(1)
            sql = "insert into got_word(word) values(%s)"
            self.cursor.execute(sql,(w,))

            print "开始搜索:%s"%w
            self.search_list(w)

            time.sleep(1)

            self.list_page = 1
            print "%s 爬取完毕，列表页重新从%s页开始爬取"%(w,self.list_page)


            sql = "delete from got_word where num = 0"
            self.cursor.execute(sql)

    def run(self):
        self.proxy = self.get_proxy()

        print "代理：%s"%self.proxy

        self.start_search()

    def search_list(self,word):
        while self.list_page < 11:
            print "开始爬取 %s 列表页第%s页..."%(word,self.list_page)
            url = self.basic_url%(word,self.list_page)

            try:
                resp = requests.get(url,headers=self.headers,proxies=self.proxy,timeout=3)
            except Exception as e:
                print str(e)
                print "代理:%s爬取失败，更换ip重新爬取..."%str(self.proxy)
                self.run()

            content = resp.content
            html = etree.HTML(content)

            weixins = html.xpath("//label/text()")
            detail_srcs = html.xpath("//li//div/p[@class='tit']/a/@href")

            if len(weixins) == 1:
                print "错误:%s,开始更换ip爬取..."%weixins[0]
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
                resp = requests.get(src,headers=self.headers,proxies=self.proxy,timeout=3)
            except Exception as e:
                print str(e)
                print "FAILED REPATE SPIDER..........."
                time.sleep(1)
                self.run()

            content = resp.content
            html = etree.HTML(content)

            heads = html.xpath("//div//span/img/@src")
            names = html.xpath("//strong/text()")

            if not names:
                print "ip被判断为非正常用户，开始更换ip爬取..."
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

if __name__ == "__main__":
    Spider().run()
