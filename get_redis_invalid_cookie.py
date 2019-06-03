import redis

r =redis.Redis(host="127.0.0.1", port=6379)

for i in range(183):
    res = r.rpoplpush('invalid_ks_cookies', 'invalid_ks_cookies').decode()
    print(res)
