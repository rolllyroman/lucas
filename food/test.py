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


headers = {
    'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
    'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
    'Connection':'Keep-Alive',
    "User-Agent":random.choice(USER_AGENTS),
}                

# browser.quit()

conn = pymysql.connect(host="119.23.52.3",user="root",passwd="168mysql",db="haha",charset="utf8")  
conn.autocommit(1) # conn.autocommit(True) 
cursor = conn.cursor()

proxies = {"http":"http://14.115.106.218:808","https":"https://125.123.139.172:9000"}
proxies = {"http":"http://14.115.106.218:808"}
proxies = {"https":"https://125.123.139.172:9000"}

# proxies = {"http":"http://180.118.128.254:9000"}

for x in range(1,10):
    for i in range(0,10):

        cookies = "SUV=00E255473B2A7BEE5B8E461231A59507; CXID=8EE8AD316575A6A993E58BBA902202E5; SUID=4A2042713965860A5B9CCFAA000A9E20; ABTEST=1|1547701774|v1; IPLOC=CN4401; weixinIndexVisited=1; SNUID=DEBD829DEDE99203B6744E35ED4C6B67; sct=8; JSESSIONID=aaamwonbHcI3WfTV8I8Cw; ad=@r9pvZllll2tSINtlllllVep70llllllnhIiKZllllwlllllVklll5@@@@@@@@@@"

        cookies = {i.split("=")[0]:i.split("=")[1] for i in cookies.split("; ")}

        url = "https://weixin.sogou.com/weixin?query=%s&_sug_type_=&s_from=input&_sug_=n&type=1&page=%s&ie=utf8"%(x,i)
        resp = requests.get(url,cookies=cookies)
        print resp.apparent_encoding
        print requests.utils.get_encodings_from_content(resp.text)
        resp.encoding = "utf-8"

        # print resp.text.encode("GBK",'ignore')
        text = resp.text

        print dir(resp)
        print resp.headers

        html = etree.HTML(text)

        weixins = html.xpath("//label/text()")
        detail_srcs = html.xpath("//li//div/p[@class='tit']/a/@href")

        for i,weixin in enumerate(weixins):    
            sql = "select weixin from robot where weixin = %s"
            cursor.execute(sql,(weixin,))
            res = cursor.fetchone()
            if res:
                continue

            print "准备进入详情页，开始获取头像和姓名..."
            src = detail_srcs[i]

            resp = requests.get(src,headers=headers,cookies=cookies)

            content = resp.content
            html = etree.HTML(content)

            heads = html.xpath("//div//span/img/@src")
            names = html.xpath("//strong/text()")

            if not names:
                print "ip被判断为非正常用户..."
                sys.exit()

            head = heads[0].replace("http","https")
            name = names[0].strip()

            sql = "insert into robot(weixin,name,head) values(%s,%s,%s)"
            cursor.execute(sql,(weixin,name,head))


            print weixin,name,head,"获取成功！！!" 

            time.sleep(1)
