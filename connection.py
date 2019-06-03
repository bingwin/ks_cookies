import pymysql
import logging
import redis


class MySQLConnection(object):
     
    def __init__(self, dbinfo={}, autocommit=True):

        self.conn = None
        self.host = dbinfo['host']
        self.database = dbinfo['dbname']
        self.user = dbinfo['user']
        self.password = dbinfo['password']
        self.port = dbinfo['port']
        self.autocommit = autocommit
    
    def get_conn(self):
 
        if not self.conn:
            self.conn = self.make_conn()
 
        return self.conn

    def make_conn(self):
 
        conn = pymysql.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            port=self.port,
            charset='utf8',
            use_unicode=True)
 
        conn.autocommit = self.autocommit
          
        logging.info("Connected to database with autocommit on: {0}.".format(self.conn))
        
        return conn

    def close_conn(self):
 
        if self.conn:
            self.conn.close()


class RedisConnection(object):
     
    def __init__(self, dbinfo={}, url=None):

        self.url = url

        self.conn = None
        self.host = dbinfo['host']
        self.port = dbinfo['port']
        # below is not used for now
        self.database = dbinfo.get('dbname')
        self.user = dbinfo.get('user')
        self.password = dbinfo.get('password')

    def get_conn(self):
 
        if not self.conn:
            self.conn = self.make_conn()
 
        return self.conn

    def make_conn(self):
 
        if self.url:
            return redis.from_url(self.url)
        else:
            logging.info("Connecting to redis database ....")
            return redis.Redis(host=self.host, port=self.port, password=self.password)

    def close_conn(self):
 
        if self.conn:
            self.conn.close()

