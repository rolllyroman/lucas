#coding:utf-8
import requests
import random
import redis

from lxml import etree
from constants import USER_AGENTS

class MyPool(object):
    
   
    local_ip = "119.23.52.3"
    # 测试ip地址
    test_url = "http://icanhazip.com/" 
    # 西刺代理
    ip_url = "https://www.xicidaili.com/nn/%s"

    def __init__(self):
        self.proxies_list = []
        self.ip_page = 1
        self.redis = redis.Redis(host='127.0.0.1', port=6379,db=1)

        self.put_proxies_list()

    def get_headers(self):
        return {
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
            'Connection':'Keep-Alive',
            "User-Agent":random.choice(USER_AGENTS),
        }

    # 开始投放有效ip代理
    def put_proxies_list(self):
        while self.ip_page < 3000:
            self.ip_page += 1
            url = self.ip_url%self.ip_page

            resp = requests.get(url,headers=self.get_headers())
            content = resp.content

            html = etree.HTML(content)

            xieyi_list = html.xpath("//tr/td[last()-4]/text()")
            port_list = html.xpath("//tr/td[last()-7]/text()")
            ip_list = html.xpath("//tr/td[last()-8]/text()")

            for i,ip in enumerate(ip_list):
                port = port_list[i]
                xieyi = xieyi_list[i].lower()

                proxies = {xieyi:"%s://%s:%s"%(xieyi,ip,port)}

                # 超时说明ip质量差 跳过
                try:
                    resp = requests.get(self.test_url,proxies=proxies,headers=self.get_headers(),timeout=1)
                except:
                    continue

                # 本机ip说明无效 跳过
                content = resp.content
                if content.startswith(self.local_ip):
                    continue

                self.redis.sadd("proxies:set",str(proxies))   
                print "%s 有效，成功入库。"


MyPool()