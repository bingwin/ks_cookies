import redis

r =redis.Redis(host="127.0.0.1", port=6379)
#r =redis.Redis(host="47.105.103.8", port=56789, password="12345678")

num = r.llen('invalid_ks_cookies')

for i in range(num):
    res = r.rpoplpush('invalid_ks_cookies', 'invalid_ks_cookies').decode()
    print(res)
