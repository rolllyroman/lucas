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

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

class Spider(object):

    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
        'Connection':'Keep-Alive',
        "User-Agent":random.choice(USER_AGENTS),
    }

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

        self.searched_word = []
        sql = "select word from got_word"
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        for r in res:
            self.searched_word.append(r[0])

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
            if w in self.searched_word:
                print "%s 已搜过，跳过..."%w
                continue

            print "开始搜索:%s"%w
            self.search_list(w)

            self.list_page = 1
            print "%s 爬取完毕，列表页重新从%s页开始爬取"%(w,self.list_page)


    def run(self):
        sql = "delete from got_word where num = 0"
        self.cursor.execute(sql)

        self.proxy = self.get_proxy()
        self.list_page = 1

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
            time.sleep(1)


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
                print "详情页响应超时...."
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


            print weixin,name,head,"获取成功！！!" 

            time.sleep(1)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

if __name__ == "__main__":
    Spider().run()
