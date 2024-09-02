#!-*- coding:utf-8 -*-
# FileName: 单连接

import redis
import pymysql


class Db:

    def __init__(self, mode: str, db_name: str = None, db_conf=None):
        self._mode = mode
        self.__db_name = db_name
        self.__db_conf = db_conf

        self.__coon = None
        self.__client = None

    @property
    def coon(self):
        return self.__coon

    @property
    def client(self):
        return self.__client

    def __enter__(self):
        if self._mode.lower() == 'mysql':
            self.__client = self.__coon = mysql_conn(self.__db_name, self.__db_conf)
        elif self._mode.lower() == 'redis':
            self.__client = self.__coon = redis_conn(self.__db_name, self.__db_conf)
        else:
            raise Exception(f'error db mode: {self._mode}')
        return self.__coon

    def __exit__(self, exc_type, exc_val, exc_tb):
        close_db(self.__coon, self.__client)


def close_db(conn, client):
    try:
        conn.close()
    except:
        pass
    try:
        client.close()
    except:
        pass


def mysql_conn(db_name, db_conf):
    conn = pymysql.connect(
        host=db_conf['host'],
        port=db_conf['port'],
        user=db_conf['user'],
        password=db_conf['password'],
        db=db_name,
        connect_timeout=15,
        charset='utf8',
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn


def redis_conn(db_name, db_conf):
    conn = redis.StrictRedis(
        host=db_conf['host'],
        port=db_conf['port'],
        password=db_conf['password'],
        db=db_name,
        decode_responses=True,      # 返回结果是否进行decode
    )
    return conn
