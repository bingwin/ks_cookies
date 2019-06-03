# -*- coding: utf-8 -*-
'''
Created on 2018年7月28日

@author: EDZ
'''
import time
import json
import requests
import logging
import random
import pymysql
from requests.exceptions import ConnectionError
from mysql import db
from selenium import webdriver
from user_agents import *
from settings import *
from headers import base_headers, bxs_headers
from connection import RedisConnection, MySQLConnection
from log import Logger

logger = Logger(logname='resource_ks_cookies.log', loglevel=logging.INFO, logger="resource").getlog()


class Resource(object):

    def __init__(self):

        self.redis_conn = RedisConnection(dbinfo=REDIS).get_conn()
        # self.data_conn = MySQLConnection(dbinfo=MYSQL_DB).get_conn()

    def get_ip(self):

        try:
            result = self.redis_conn.llen(HTTPS_PROXY_IP_POOL)
            if result > 0:
                ip_li = []

                # 使用5个IP多线程同时请求Cookie
                for i in range(3):
                    res = self.redis_conn.rpoplpush(HTTPS_PROXY_IP_POOL, HTTPS_PROXY_IP_POOL).decode()
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

    def get_webpage(self):

        pros = self.get_ip()
        # pro = 1

        if pros:
            for proxy in pros:
                options = webdriver.ChromeOptions()
                # options.binary_location = r"D:\software_location\cent_install\CentBrowser\Application\chrome.exe"
                options.binary_location = '/usr/bin/google-chrome-stable'

                # Linux 环境下配置
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-extensions')
                options.add_argument('--disable-gpu')

                logging.info('使用IP %s ...' % (proxy))
                options.add_argument("--proxy-server=http://%s" % (proxy))

                driver = webdriver.Chrome(executable_path='/home/seeta/zhangyanchao/chromedriver_install/chromedriver',
                                          chrome_options=options)
                # driver = webdriver.Chrome(executable_path='D:\projects\Weibo_projects\chromedriver.exe',
                #                           chrome_options=options)

                # # 设置代理
                # # options.add_argument("--proxy-server=http://%s" % (pro))
                # options.add_argument("--proxy-server=http://%s" % ('119.129.236.251:4206'))

                # # 使用 PhantomJS 初始化
                # service_args = ['--proxy=119.129.236.251:4206', '--proxy-type=socks5', ]
                # driver = webdriver.PhantomJS(r'C:\Users\Administrator\Desktop\phantomjs-2.1.1-windows\phantomjs-2.1.1-windows\bin\phantomjs.exe', service_args=service_args)

                # # 一定要注意，=两边不能有空格，不能是这样--proxy-server = http://202.20.16.82:10152
                # driver = webdriver.Chrome(chrome_options=options)
                # driver.maximize_window()

                # # 查看本机ip，查看代理是否起作用
                # driver.get("http://httpbin.org/ip")
                # print(driver.page_source)

                driver.get('https://live.kuaishou.com/')
                cookies = driver.get_cookies()
                # print(driver.page_source)
                logging.warning(cookies)
                if '未连接到互联网' in driver.page_source or not cookies:
                    logging.warning('访问快手首页出现问题, 重新请求新的IP并访问...')
                    driver.quit()
                    pass
                    # self.get_webpage()  # 此处可能陷入死循环

                else:
                    cookie = {}
                    for res in cookies:
                        name = res['name']
                        value = res['value']
                        # print(res['name'], res['value'])
                        cookie[name] = value
                    cookie_d = "{'cookie':" + str(cookie) + '}'  # 插入后还有双引号, 可能影响结果
                    logging.warning(cookie_d)

                    # 上传到服务器
                    self.redis_conn.lpush('ks_cookies', cookie_d)

                    people_li = ['dagaoge666', 'meishi123458888', 'wangzulan', '3xgghwn46skhkxa', 'sanda927', 'hs1590ai', 'xiaoyiyi', '3xjb64qxiwbv2dm', 'huangbo666', 'Sanmei1997']
                    driver.get('https://live.kuaishou.com/profile/%s' % (random.choice(people_li)))
                    logging.info('获取首页成功, 刷新页面...')
                    for i in range(2):
                        driver.refresh()
                    # 退出，清除浏览器缓存
                    time.sleep(5)
                    driver.quit()
                    logging.info('退出浏览器 ...')

    def scan_verify_cookie_pool(self, cookie_pool):

        logger.info("%s代理池资源总数：%s" % (cookie_pool, self.redis_conn.llen(cookie_pool)))
        valid_count = 0
        invalid_count = 0
        test_count = 1
        date_format = '%Y-%m-%d %H:%M:%S'

        while True:
            try:
                result = self.redis_conn.llen(cookie_pool)
                if result < FILL_RESOURCE_THRESHOLD:
                    self.get_webpage()

                time.sleep(7)
                logging.warning('检测代理池时间...')
            except:
                logging.warning('获取页面时程序发生错误 ...')
                time.sleep(30)


if __name__ == '__main__':
    resource = Resource()
    resource.scan_verify_cookie_pool(HTTPS_PROXY_COOKIE_POOL)
