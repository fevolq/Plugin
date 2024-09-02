#!-*- coding:utf-8 -*-
# Filename: 连接池

import atexit
import hashlib

import redis
from dbutils.pooled_db import PooledDB
import pymysql.cursors


class PoolDB:

    __pools = {}  # key: PooledDB()

    def __init__(self, mode: str, db_name, db_conf):
        self._mode = mode
        self._db_name = db_name
        self._db_conf = db_conf

        self.__key = hashlib.md5(f'{self._mode}/{self._db_name}/{self._db_conf}'.encode(encoding='UTF-8')).hexdigest()
        if self.__key not in PoolDB.__pools:
            self._prepare()
        self.__pool = PoolDB.__pools[self.__key]

    @property
    def key(self):
        return self.__key

    def _prepare(self):
        if self._mode.lower() == 'mysql':
            creator = pymysql
            host = self._db_conf['host']
            port = self._db_conf['port']
            user = self._db_conf['user']
            password = self._db_conf['password']
            database = self._db_name

            pool = PooledDB(
                creator=creator,
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                autocommit=True,
                charset='utf8mb4',
                read_timeout=20,
                write_timeout=60,
                maxconnections=100,
                mincached=3,
                maxusage=30,
                blocking=True,
                cursorclass=pymysql.cursors.DictCursor,
                ping=7
            )
        elif self._mode.lower() == 'redis':
            host = self._db_conf['host']
            port = self._db_conf['port']
            password = self._db_conf['password']
            database = self._db_name

            pool = redis.ConnectionPool(
                host=host,
                port=port,
                password=password,
                db=database,
                max_connections=100,
                decode_responses=True,
            )
        else:
            raise Exception(f'error db mode: {self._mode}')
        PoolDB.__pools[self.__key] = pool

    def get_connection(self):
        coon = None
        if self._mode == 'mysql':
            coon = self.__pool.connection()
        elif self._mode == 'redis':
            coon = redis.Redis(connection_pool=self.__pool)
        return coon

    @classmethod
    def close_pool(cls, key=None):

        def close(pool):
            try:
                pool.close()
            except:
                pass

        if key:
            close(cls.__pools.get(key))
        else:
            for key in cls.__pools:
                close(cls.__pools.get(key))


def get_coon(mode: str = 'mysql', **kwargs):
    """

    :param mode: 使用的模式
    :param kwargs:
    :return:
    """
    db_name = kwargs.get('db_name', None)
    db_conf = kwargs.get('db_conf', None)

    dbpool = PoolDB(mode, db_name, db_conf)
    return dbpool.get_connection()


def close_pool(key=None):
    return PoolDB.close_pool(key=key)


@atexit.register
def close_all_pool():
    return close_pool()
