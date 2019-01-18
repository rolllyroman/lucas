import requests
import time
from lxml import etree
import json

with open("players.json","r") as f:
    content = f.read()
    players = json.loads(content)


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


def main():
    headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept - Encoding':'gzip, deflate',
               'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection':'Keep-Alive',
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}

    for cat in ["star","grass","content"]:

        print cat

        url = "https://weibo.cn/pub/top?cat="+cat+"&page=%s"
        for page in range(1,11):

            print page

            resp = requests.get(url%page,headers=headers)
            deal_content(resp)

            time.sleep(1)

    print players

    with open("robots.json","w") as f:
        f.write(json.dumps(players))


if __name__ == "__main__":
    main()
