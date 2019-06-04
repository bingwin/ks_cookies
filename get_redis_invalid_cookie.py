import redis

r =redis.Redis(host="127.0.0.1", port=6379)
#r =redis.Redis(host="47.105.103.8", port=56789, password="12345678")

for i in range(30):
    res = r.rpoplpush('ks_cookies', 'ks_cookies').decode()
    print(res)
