# -*- coding:utf-8 -*-
import re
import json
import time
from multiprocessing import Pool
import requests
import redis


# db_local = redis.StrictRedis(host="127.0.0.1", port="6379")
# db = redis.StrictRedis(host="172.181.217.58", port="6379")
db = redis.StrictRedis(host="47.105.103.8", port="56789", password="12345678")
PROXY_POOL = 'invalid_https_proxy'
# PROXY_POOL = 'invalid_history_bxs_proxy'


def tip(proxy, ip_li):  # 多进程检测代理池
    try:
        proxies = {

            "http": proxy,
            "https": proxy,
        }
        VALID_STATUS_CODES = [200, 302]
        # targetUrl = "http://members.3322.org/dyndns/getip"
        targetUrl = "http://www.baidu.com/"
        response = requests.get(targetUrl, proxies=proxies, timeout=12, allow_redirects=False)
        # print('1111111111', response.text)
        if response.status_code in VALID_STATUS_CODES:
            print('代理: ', proxy, ' 可用')
            ip_li.append(proxy)
            print(11111111111)
            # TODO 判断 https_proxy 是否已经有了对应的Ip

            if proxy.encode() in db.lrange('https_proxy', 0, -1):
                print('IP已经存在...')
                db.lrem('invalid_https_proxy', 0, proxy)
                print('删除已经插入的ip...')
            else:
                db.lpush('https_proxy', proxy)
                print('检测有效, 插入到 https_proxy...')
                db.lrem('invalid_https_proxy', 0, proxy)
                print('删除已经插入的ip...')
        else:
            print('请求响应码不合法', response.status_code, 'IP', proxy)
    except Exception as e:
        print('错误提示: ', e.args)
        # db.hdel('https_proxy', key)
        # db.hset('invalid_history_bxs_proxy', key, value)
        print('代理请求失败', proxy, ' 已删除')


def run(proxy, bind_key, bind_value):

    pool = Pool(10)
    ip_li = []
    for proxy1 in proxy:
        pool.apply_async(tip, (proxy1, ip_li))
    print('------start--------')
    pool.close()
    pool.join()
    print('-------end---------')



def get_proxy():
    num = db.llen(PROXY_POOL)
    print("代理池总数量是:", num)

    proxy_li = []
    bind_key = []
    bind_value = []
    for i in range(0, num):
        print(db.lindex("invalid_https_proxy", i))
        print(type(db.lindex("invalid_https_proxy", i)))
        proxy_1 = db.lindex("invalid_https_proxy", i).decode()
        proxy = re.sub(r'https?://', '', proxy_1)
        proxy_li.append(proxy)
    print('代理列表proxy_li:', proxy_li)
    print('代理列表长度:', len(proxy_li))
    return proxy_li, bind_key, bind_value


def main():

    proxy, bind_key, bind_value = get_proxy()
    run(proxy, bind_key, bind_value)


if __name__ == '__main__':

    # db = redis.StrictRedis(host="120.92.105.253", port="56789", password="12345678@redis.com")
    db = redis.StrictRedis(host="47.105.103.8", port="56789", password="12345678")
    # db = redis.StrictRedis(host="172.181.217.58", port="6379")
    while 1:
        time.sleep(10)
        main()
