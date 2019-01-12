import requests
import time


def deal_content(resp):
    content = resp.content.decode()
    print "="*77
    print content
    print "="*77

def main():
    url = "https://weibo.cn/pub/top?cat=star&page=%s"
    for page in range(2,11):
        resp = requests.get(url%page)
        deal_content(resp)

        time.sleep(1)

