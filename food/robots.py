#coding:utf-8
import requests
import time
from lxml import etree
import json

import MySQLdb

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

# with open("robots.json","r") as f:
#     content = f.read()
#     players = json.loads(content)

HEADERS = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
           'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
           'Connection':'Keep-Alive',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}

BASIC_URL = "https://weixin.sogou.com/weixin?query=%s&_sug_type_=&s_from=input&_sug_=n&type=1&page=%s&ie=utf8"

conn = MySQLdb.connect(host="119.23.52.3",user="root",passwd="168mysql",db="haha",charset="utf8")  
cursor = conn.cursor()

def search_list(word):
    for i in range(1,11):
        url = BASIC_URL%(word,i)
        resp = requests.get(url,headers=HEADERS)
        html = etree.HTML(resp.content)
        # img_srcs = html.xpath("//li//div[@class='img-box']//img/@src")
        detail_srcs = html.xpath("//li//div/p[@class='tit']/a/@href")

        for src in detail_srcs:
            resp = requests.get(src,headers=HEADERS)
            html = etree.HTML(resp.content)
            head = html.xpath("//div//span/img/@src")[0].replace("http","https")
            name = html.xpath("//strong/text()")[0]

            print '-----------------------'
            print name,head

            time.sleep(10)

def get_words():
    words = set()
    url = "https://hanyu.baidu.com/shici/detail?pid=0b2f26d4c0ddb3ee693fdb1137ee1b0d&from=kg0"
    resp = requests.get(url,headers=HEADERS)

    # print resp.content.decode("gb2312")
    resp.encoding = "utf-8"
    html = resp.text

    for w in html:
        words.add(w)
    return words

def main():
    words = get_words()
    for w in words:
        pass


def test():

    url = "https://weixin.sogou.com/weixin?query=%E6%9D%8E&_sug_type_=&s_from=input&_sug_=n&type=1&page=2&ie=utf8"
    resp = requests.get(url,headers=HEADERS)
    
    html = etree.HTML(resp.content)
    # img_srcs = html.xpath("//li//div[@class='img-box']//img/@src")
    detail_srcs = html.xpath("//li//div/p[@class='tit']/a/@href")

    for src in detail_srcs:
        resp = requests.get(src,headers=HEADERS)
        html = etree.HTML(resp.content)
        head = html.xpath("//div//span/img/@src")[0].replace("http","https")
        name = html.xpath("//strong/text()")[0]

        sql = "insert into robot(name,head) values(%s,%s)"
        cursor.execute(sql,(name,head))

        time.sleep(2)


if __name__ == "__main__":
    # main()
    test()
