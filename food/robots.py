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


from constant import USER_AGENT

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chromeOptions = webdriver.ChromeOptions()

# 设置代理
chromeOptions.add_argument("--proxy-server=http://112.85.167.11:9999")
# 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
driver = webdriver.Chrome(chrome_options = chromeOptions)

# 设置无头
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# driver = webdriver.Chrome(chrome_options=chrome_options)

# driver = webdriver.Chrome()


HEADERS = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
           'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
           'Connection':'Keep-Alive',
           # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
            'User-Agent':random.choice(USER_AGENT),
           }


BASIC_URL = "https://weixin.sogou.com/weixin?query=%s&_sug_type_=&s_from=input&_sug_=n&type=1&page=%s&ie=utf8"

conn = pymysql.connect(host="119.23.52.3",user="root",passwd="168mysql",db="haha",charset="utf8")  
conn.autocommit(1) # conn.autocommit(True) 
cursor = conn.cursor()

proxies_queue = []

# def put_proxy_queue():
#     url = "https://proxyapi.mimvp.com/api/fetchsecret.php?orderid=862060912114100297&num=5&http_type=3&result_fields=1,2,3"
#     resp = requests.get(url)

#     content = resp.content
#     datas = content.split('\r\n')

#     for data in datas:
#         http_ip = data.split(',')[0]
#         https_ip = http_ip.split(":")[0] + data.split(',')[-1]

#         proxies = {
#             "http":http_ip,
#             "https":https_ip,
#         } 

#         try:
#             print "测试结果：%s"%requests.get("http://www.baidu.com",proxies=proxies)
#         except:
#             print "失败proxies:%s"%proxies
#         else:
#             proxies_queue.append(proxies)

#     print "now proxies_queue:%s"%proxies_queue


# def get_proxies():
#     print "now proxies_queue:%s"%proxies_queue

#     if len(proxies_queue) < 20:
#         for i in range(1,6):
#             print "wait for put proxy... %s"%i
#             time.sleep(1)

#         put_proxy_queue()
        
#     res = random.choice(proxies_queue)

#     try:
#         requests.get("http://www.baidu.com",proxies=res)
#     except:
#         proxies_queue.remove(res)
#         return get_proxies()
#     else:
#         return res 

def if_list_code(weixins,detail_srcs):
    if len(weixins) == 1:
        code = raw_input("请输入验证码：")
        code_label = driver.find_element_by_name("c")
        code_label.send_keys(" ") # 防止发送不成功
        code_label.clear()
        code_label.send_keys(code) 

        submit_label = driver.find_element_by_id("submit")
        submit_label.click()

        time.sleep(1)
        content = driver.page_source.encode("utf-8")

        html = etree.HTML(content)

        weixins = html.xpath("//label/text()")
        detail_srcs = html.xpath("//li//div/p[@class='tit']/a/@href")

        print "weixins:%s"%weixins

        if len(weixins) == 1:
            return if_list_code(weixins,detail_srcs)

    return weixins,detail_srcs


def search_list(word):
    print "search_list:%s"%word
    for i in range(1,11):
        url = BASIC_URL%(word,i)
        # resp = requests.get(url,headers=HEADERS)
        driver.get(url)

        time.sleep(1)

        content = driver.page_source.encode("utf-8")
        html = etree.HTML(content)

        # print resp.content.decode()
        # print "============="
        # print url
        # print "============="
        # print resp.status_code

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


def if_detail_code(heads,names):
    # 弹出详情验证码
    if not names:
        code = raw_input("请输入验证码:")
        code_label = driver.find_element_by_id("input")
        code_label.send_keys(" ") # 防止发送不成功
        code_label.clear()
        code_label.send_keys(code) 

        submit_label = driver.find_element_by_id("bt")
        submit_label.click()

        time.sleep(1)
        content = driver.page_source.encode("utf-8")
        html = etree.HTML(content)

        heads = html.xpath("//div//span/img/@src")
        names = html.xpath("//strong/text()")

        if not names:
            return if_detail_code(heads,names)

    return heads,names


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

# def test2():
#     url = "https://weixin.sogou.com/weixin?query=%E6%9D%8E&_sug_type_=&s_from=input&_sug_=n&type=1&page=222&ie=utf8"
#     resp = requests.get(url,headers=HEADERS)
#     html = etree.HTML(resp.content)

#     weixins = html.xpath("//label/text()")

#     print "==========================="
#     print weixins
#     print "==========================="


if __name__ == "__main__":
    main()
    cursor.close()
    conn.close()
    driver.close()
