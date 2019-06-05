# -*- coding: utf-8 -*-
'''
Created on 2018年7月28日

@author: EDZ
'''
import time
import json
import redis
import random
import pymysql
import logging
import datetime
import requests
from mysql import db
from settings import *
from log import Logger
from user_agents import *
from selenium import webdriver
from sshtunnel import SSHTunnelForwarder
from headers import base_headers, bxs_headers
from requests.exceptions import ConnectionError
from connection import RedisConnection, MySQLConnection

logger = Logger(logname='monitor_ks_cookies.log', loglevel=logging.INFO, logger="resource").getlog()


class Resource(object):

    def __init__(self):

        # self.redis_conn = RedisConnection(dbinfo=REDIS).get_conn()

        # 使用SSHTunnelForwarder隧道，通过跳板机链接Redis
        server = SSHTunnelForwarder(
            ('58.213.140.158', 22),  # 跳板机
            ssh_username='seetatech',
            ssh_password="SeetaWin@161202",
            remote_bind_address=('172.181.217.58', 6379),  # 远程的Redis服务器
            local_bind_address=('0.0.0.0', 10022)  # 开启本地转发端口
        )
        server.start()  # 开启隧道

        # 本地通过local_bind_port端口转发，利用跳板机，链接Redis服务
        self.redis_conn = redis.Redis(host='127.0.0.1', port=server.local_bind_port, decode_responses=True)

        # for i in range(50):
        #     res = self.redis_conn.rpoplpush('invalid_ks_cookies', 'invalid_ks_cookies')
        #     print(res)

        # server.close()  # 关闭隧道

    def get_ip(self):

        try:
            result = self.redis_conn.llen(HTTPS_PROXY_IP_POOL)
            if result > 0:
                ip_li = []

                # 使用5个IP多线程同时请求Cookie
                for i in range(1):
                    res = self.redis_conn.rpoplpush(HTTPS_PROXY_IP_POOL, HTTPS_PROXY_IP_POOL)
                    ip_li.append(res)

                return ip_li

            else:
                logging.warning('获取Cookie时请求的IP池为空...')
                time.sleep(30)

        except:
            logging.warning('获取Cookie时请求IP池发生错误...')
            time.sleep(30)

    def verify_ip(self):

        proxy = self.get_ip()

        real_proxy = {
            'http': proxy,
            'https': proxy
        }
        url = 'http://www.baidu.com/'
        res = requests.get(url, proxies=real_proxy)
        if res.status_code == 200:
            return proxy
        else:
            return False

    def get_webpage(self, cookiess):

        pros = self.get_ip()
        # pros = [1]

        if pros:
            for proxy in pros:
                options = webdriver.ChromeOptions()
                options.binary_location = r"D:\software_location\cent_install\CentBrowser\Application\chrome.exe"
                # options.binary_location = '/usr/bin/google-chrome-stable'

                # # Linux 环境下配置
                # options.add_argument('--headless')
                # options.add_argument('--no-sandbox')
                # options.add_argument('--disable-extensions')
                # options.add_argument('--disable-gpu')

                options.add_argument("--proxy-server=http://%s" % (proxy))
                # options.add_argument("--proxy-server=http://%s" % ('60.182.165.112:4231'))

                # driver = webdriver.Chrome(executable_path='/home/seeta/zhangyanchao/chromedriver_install/chromedriver',
                #                           chrome_options=options)
                driver = webdriver.Chrome(executable_path='D:\projects\Weibo_projects\chromedriver.exe',
                                          chrome_options=options)

                # 查看本机ip，查看代理是否起作用
                # driver.set_page_load_timeout(5)
                driver.get("http://httpbin.org/ip")  # 技术提示：必须首先加载网站，这样Selenium 才能知道cookie 属于哪个网站，即使加载网站的行为对我们没任何用处
                if '未连接到互联网' in driver.page_source:
                    logging.warning('访问快手首页出现问题, 关闭浏览器...')
                    driver.quit()
                    logging.warning('把 Cookie 重新放入 invalid_cookies 池中...')
                    self.redis_conn.lpush(INVALID_KS_COOKIE_POOL, cookiess)
                else:
                    # driver.get("http://www.baidu.com/")
                    try:
                        expires = str(self.get_time())
                        for k, v in cookiess['cookie'].items():
                            driver.add_cookie({
                                'domain': '.kuaishou.com',
                                'name': k,
                                'value': v,
                                'path': '/',
                                'expires': expires

                            })

                        people_li = ['dagaoge666', 'TS-J0315J', 'meishi123458888', 'lol1314666', 'travelers', 'dingdang660', 'xue66666', 'wangzulan', '3xgghwn46skhkxa', 'sanda927', 'hs1590ai', 'xiaoyiyi', '3xjb64qxiwbv2dm', 'huangbo666', 'Sanmei1997']

                        driver.get('https://live.kuaishou.com/profile/%s' % (random.choice(people_li)))

                        if '未连接到互联网' in driver.page_source:
                            logging.warning('访问快手首页出现问题, 关闭浏览器...')
                            driver.quit()
                            logging.warning('把 Cookie 重新放入 invalid_cookies 池中...')
                            self.redis_conn.lpush(INVALID_KS_COOKIE_POOL, str(cookiess))

                        else:
                            for i in range(1):
                                time.sleep(0.3)
                                driver.refresh()

                            # 刷新后重新插入 Cookies 池
                            logging.info('使用 %s 刷新成功, 放入 正常Cookies池中...' % (cookiess))
                            print('使用 %s 刷新成功, 放入 正常Cookies池中...' % (cookiess))
                            self.redis_conn.lpush(HTTPS_PROXY_COOKIE_POOL, str(cookiess))

                            # 退出，清除浏览器缓存
                            time.sleep(4)
                            driver.quit()
                    except Exception as e:
                        logging.warning('赋值 Cookie 时发生错误 %s' % (e))
                        logging.warning('把 Cookie 重新放入 invalid_cookies 池中...')
                        self.redis_conn.lpush(INVALID_KS_COOKIE_POOL, str(cookiess))
                        driver.quit()

    def scan_verify_cookie_pool(self, cookie_pool):

        logger.info("%s代理池资源总数：%s" % (cookie_pool, self.redis_conn.llen(cookie_pool)))
        valid_count = 0
        invalid_count = 0
        test_count = 1
        date_format = '%Y-%m-%d %H:%M:%S'

        while True:
            try:
                result = self.redis_conn.llen(cookie_pool)  # 后期如果重复严重改成 set
                if result > 0:
                    # cookiess = json.loads(self.redis_conn.rpop(cookie_pool).decode().replace("'", '"'))
                    cookiess = json.loads(self.redis_conn.rpop(cookie_pool).replace("'", '"'))
                    # self.redis_conn.lpush(cookie_pool, str(cookiess)) # 测试使用
                    self.get_webpage(cookiess)
                else:
                    time.sleep(3)  # 如果 Cookie 淤积太多修改睡眠时间
                    logging.warning('检测代理池时间...')
            except Exception as e:
                print(e)
                time.sleep(3)

    def get_time(self):

        bb = datetime.datetime.now() + datetime.timedelta(days=365)
        d = datetime.datetime.strptime(str(bb), "%Y-%m-%d %H:%M:%S.%f")
        t = d.timetuple()
        timeStamp = int(time.mktime(t))
        timeStamp = float(str(timeStamp) + str("%06d" % d.microsecond)) / 1000000
        print('timeStamp', timeStamp)
        return timeStamp


if __name__ == '__main__':
    resource = Resource()
    resource.scan_verify_cookie_pool(INVALID_KS_COOKIE_POOL)
