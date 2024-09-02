from typing import List

from dao import redisDB, mysqlDB


def execute_redis(args, *, kwargs, db_name, action):
    args = args or []
    kwargs = kwargs or {}
    result = redisDB.execute(action, *args, **kwargs, db_name=db_name, raise_error=False)
    res = {'code': 200 if result['success'] else 400}
    if result['success']:
        res['data'] = result['result']
    else:
        res['msg'] = result['result']

    return res


def execute_mysql(sql: str, args: List, *, db_name: str):
    result = mysqlDB.execute(sql, args, db_name=db_name, raise_error=False)
    res = {'code': 200 if result['success'] else 400}
    if result['success']:
        res['data'] = result['result']
    else:
        res['msg'] = result['result']

    return res
