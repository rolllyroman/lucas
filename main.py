import requests
import time
from lxml import etree

def deal_content(resp):
    content = resp.content
    # print "="*77
    # print content
    # print "="*77
    html = etree.HTML(content)

    img_srcs = html.xpath("/html/body//td/a/img/@src")
    names = html.xpath("/html/body//td[last()]/a[last()-1]")

    for i,name in enumerate(names):
        src = img_srcs[i]
        print name,src


def main():

    headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept - Encoding':'gzip, deflate',
               'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection':'Keep-Alive',
               'Host':'zhannei.baidu.com',
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}

    url = "https://weibo.cn/pub/top?cat=star&page=%s"
    for page in range(2,11):
        resp = requests.get(url%page,headers=headers)
        deal_content(resp)

        time.sleep(1)


if __name__ == "__main__":
    main()

