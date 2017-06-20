import redis

conn = redis.StrictRedis(host='redis', port=6379, db=0)


def dummy_auth(username, password):
    if username in conn.keys():
        return conn.get(username) == password
    else:
        conn.set(username, password)
        return True
