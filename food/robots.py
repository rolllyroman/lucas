#coding:utf-8
import requests
import time
from lxml import etree
import json


# with open("robots.json","r") as f:
#     content = f.read()
#     players = json.loads(content)

HEADERS = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
           'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
           'Connection':'Keep-Alive',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}

def deal_content(resp):
    content = resp.content

    # print "="*77
    # print content
    # print "="*77

    html = etree.HTML(content)

    img_srcs = html.xpath("/html/body//td/a/img/@src")
    names = html.xpath("/html/body//td[last()]/a[last()-1]/text()")


    for i,name in enumerate(names):
        src = img_srcs[i]
        players[name] = src

def get_words():
    words = set()
    url = "https://hanyu.baidu.com/shici/detail?pid=0b2f26d4c0ddb3ee693fdb1137ee1b0d&from=kg0"
    resp = requests.get(url,headers=HEADERS)
    for w in resp.content:
        words.add(w)
    return words

def main():
    words = get_words()
    print words
    for w in words:
        print w


if __name__ == "__main__":
    main()
