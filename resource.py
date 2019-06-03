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
from user_agents import *
from settings import *
from headers import base_headers, bxs_headers
from connection import RedisConnection, MySQLConnection
from log import Logger

logger = Logger(logname='resource.log', loglevel=logging.INFO, logger="resource").getlog()


class Resource(object):
    
    def __init__(self):

        self.redis_conn = RedisConnection(dbinfo=REDIS).get_conn()
        # self.data_conn = MySQLConnection(dbinfo=MYSQL_DB).get_conn()

    def request_proxy_ip(self, url, number):
        
        # request_url = url + '&count=' + str(number) # 蘑菇代理
        request_url = url + '&num=' + str(number) # 芝麻代理
        # request_url = url + '&number=' + str(number) # 快代理

        try:
            response = requests.get(request_url, headers=base_headers)
            if response.status_code == 200:
                result = json.loads(response.text)
                logger.info(result)
                # if result.get('success'):
                if result.get('data'):
                    logger.info('%s 成功获取%s个代理' % (time.asctime(), len(result['data'])))
                    print(result['data'])
                    return result['data'] # proxies are returned here
                else:
                    logger.error('%s 获取%s个代理失败，URL: %s' % (time.asctime(), number, request_url))
        except Exception as e:
            logger.error('%s 获取%s个代理失败，URL: %s' % (time.asctime(), number, request_url))
            logger.error('错误：%s' % e)
        
    def load_proxy_pool(self, protocol, proxies):
        
        for proxy in proxies:
            
            if protocol == 'https':
            
                # proxy_item = {"port": proxy, "user": 'user', "pass": 'pass', "status": "A", "enter_time": int(time.time()), "invalid_time": 0, "success": 0, "fail": 0}
                proxy_item = '%s:%s'%(proxy['ip'], proxy['port'])
                # self.redis_conn.hset(HTTPS_PROXY_IP_POOL, proxy['ip'], str(proxy_item))
                self.redis_conn.lpush(HTTPS_PROXY_IP_POOL, proxy_item)
                logger.info("Added new proxy %s:%s into proxy pool: %s" % (proxy['ip'], proxy['port'], HTTPS_PROXY_IP_POOL))
            
    def get_new_proxy(self, number=PROXY_REQUEST_CHUNK):
        
        # 请求新的代理IP
        logger.info("request new proxy IP")
        proxies = self.request_proxy_ip(PROXY_REQUEST_URL, number)
        if proxies:
            logger.info("load new proxy IP")
            self.load_proxy_pool('https', proxies)
            # self.load_proxy_into_db(proxies)
            
    def scan_verify_proxy_pool(self, proxy_pool):

        logger.info("%s代理池资源总数：%s" % (proxy_pool, self.redis_conn.llen(proxy_pool)))
        valid_count = 0
        invalid_count = 0
        test_count = 1
        date_format = '%Y-%m-%d %H:%M:%S'

        while True:
            try:
                result = self.redis_conn.llen(proxy_pool)
                if result < FILL_RESOURCE_THRESHOLD:
                    self.get_new_proxy()

                time.sleep(10)
                print('检测代理池时间...')
            except :

                time.sleep(30)

    def get_resource_pool_size(self):
        
        return self.redis_conn.llen(BXS_RESOURCE_POOL)

                
if __name__ == '__main__':

    resource = Resource()
    resource.scan_verify_proxy_pool(HTTPS_PROXY_IP_POOL)
