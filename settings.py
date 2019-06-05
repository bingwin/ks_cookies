# MYSQL_DB = {
# 'host' : '120.92.79.194',
#   'user': 'crawler',
#   'password' : 'Cradmin@567',
#   'dbname' : 'crawler',
#   'port' : 3306
# }

# REDIS = {
#     'url': None,
# #     'host': 'localhost',
#     'host': '120.92.105.253',
#     'port': 56789,
#     'password': '12345678@redis.com'
#     }

MYSQL_DB = {
'host' : '47.105.103.8',
  'user': 'root',
  'password' : 'Mysql@1234',
  'dbname' : 'ali_crawler',
  'port' : 3306
}

# REDIS = {
#     'url': None,
# #     'host': 'localhost',
#     'host': '47.105.103.8',
#     'port': 56789,
#     'password': '12345678'
#     }


REDIS = {
    'url': None,
    'host': '172.181.217.58',
    'port': 6379,
    }

BXS_COOKIE_POOL = 'bxs_cookies' # HASH
MOBILE_UA_POOL = 'mobile_ua'    # LIST

HTTPS_PROXY_IP_POOL = 'https_proxy' # HASH
HTTPS_PROXY_COOKIE_POOL = 'ks_cookies'
INVALID_KS_COOKIE_POOL = 'ks_cookies' # TODO 0605
# INVALID_KS_COOKIE_POOL = 'invalid_ks_cookies'

BXS_RESOURCE_POOL = 'bxs_resource'  # LIST
INVALID_BXS_RESOURCE_POOL = 'invalid_bxs_resource' # LIST
INVALID_BXS_RESOURCE_HISTORY_POOL = 'invalid_history_bxs_resource' # LIST
INVALID_BXS_COOKIE_HISTORY_POOL = 'invalid_history_bxs_cookie' # HASH
INVALID_BXS_PROXY_HISTORY_POOL = 'invalid_history_bxs_proxy' # HASH

CHECK_INVALID_POOL_CYCLE = 30
CHECK_RESOURCE_POOL_CYCLE = 60
TEST_RESOURCE_CYCLE = 60
FILL_RESOURCE_THRESHOLD = 50000

# PROXY_REQUEST_URL = 'http://webapi.http.zhimacangku.com/getip?type=2&pro=&city=0&yys=0&port=11&time=2&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions=&'
# PROXY_REQUEST_URL = 'http://webapi.http.zhimacangku.com/getip?type=2&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='
# PROXY_REQUEST_URL = 'http://webapi.http.zhimacangku.com/getip?type=2&pro=&city=0&yys=0&port=1&pack=44051&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='
# PROXY_REQUEST_URL = 'http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=1eb26c3afcca421596e40c0c58f98705&expiryDate=0&format=1&newLine=2'
# PROXY_REQUEST_URL = 'http://webapi.http.zhimacangku.com/getip?type=2&pro=&city=0&yys=0&port=11&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='
# PROXY_REQUEST_URL = 'http://webapi.http.zhimacangku.com/getip?type=2&pro=&city=0&yys=0&port=11&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='

PROXY_REQUEST_CHUNK = 1

PROXY_TABLE = 'proxy_zhima'
