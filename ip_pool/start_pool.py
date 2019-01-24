#coding:utf-8
import requests
import random
import redis
import threading

from lxml import etree
from constants import USER_AGENTS

class BasePool(threading.Thread):
    
   
    local_ip = "119.23.52.3"
    # 测试ip地址
    test_url = "http://icanhazip.com/" 
    # 西刺代理
    ip_url = "https://www.xicidaili.com/nn/%s"

    def __init__(self):
        self.proxies_list = []
        self.ip_page = 1
        self.redis = redis.Redis(host='127.0.0.1', port=6379,db=1)

        threading.Thread.__init__(self) 

    def get_headers(self):
        return {
            'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
            'Connection':'Keep-Alive',
            "User-Agent":random.choice(USER_AGENTS),
        }

class PutPool(BasePool):

    # 开始投放有效ip代理
    def run(self):
        while 1:
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

                    if xieyi not in ["http","https"]:
                        continue

                    proxies = {xieyi:"%s://%s:%s"%(xieyi,ip,port)}

                    try:
                        resp = requests.get(self.test_url,proxies=proxies,headers=self.get_headers(),timeout=1)
                    except:
                        print "%s 超时,跳过..."%ip
                        continue

                    # 本机ip说明无效 跳过
                    content = resp.content
                    if content.startswith(self.local_ip):
                        print "%s 失效,跳过..."%ip
                        continue

                    self.redis.sadd("proxies:set",str(proxies))   
                    print "%s 有效，成功入库。"%ip

class CheckPool(BasePool):
    def run(self):
        while 1:
            proxies_set = self.redis.smembers("proxies:set")
            num = len(proxies_set)
            print "当前入库有效ip数量%s"%num
            time.sleep(1)
            for proxies in proxies_set:
                ip = eval(proxies).values()[-]
                try:
                    resp = requests.get(self.test_url,proxies=proxies,headers=self.get_headers(),timeout=1)
                except:
                    print "入库中的ip %s 超时,出库..."%eval(proxies).keys()
                    self.redis.srem("proxies:set",proxies)
                    continue

                # 本机ip说明无效 跳过
                content = resp.content
                if content.startswith(self.local_ip):
                    print "入库中的ip %s 失效,出库..."%ip
                    self.redis.srem("proxies:set",proxies)
                    continue

                print "入库中的ip %s 有效,开始检测下一个..."%ip


if __name__ == "__main__":
    t1 = PutPool()
    t2 = CheckPool()
    t1.start()
    t2.start()

    t1.join()
    t2.join()