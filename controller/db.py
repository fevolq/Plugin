from typing import Any, Union, List

from fastapi import APIRouter, Query
from pydantic import BaseModel

import config
from module.db import logic
from utils import log_sls

prefix = 'db'
router = APIRouter(
    prefix=f'/{prefix}',
    tags=[prefix],
)


class RedisQuery(BaseModel):
    action: str
    db_name: Union[int, str] = Query(default=0)
    args: List[Any] = Query(default=[])
    kwargs: dict = Query(default={})


@router.post("/redis", description='执行redis')
def execute_redis(req: RedisQuery):
    log_sls.info(f'{prefix}/redis', '接收参数',
                 db_name=req.db_name, action=req.action, args=req.args, kwargs=req.kwargs)
    res = logic.execute_redis(req.args, db_name=req.db_name, action=req.action, kwargs=req.kwargs)
    return res


class MysqlQuery(BaseModel):
    db_name: str = Query(default=config.MYSQL_DB)
    sql: str = Query(default=..., description='SQL语句')
    args: List[Any] = Query(default=[], description='值')


@router.post("/mysql", description='执行mysql')
def execute_mysql(req: MysqlQuery):
    log_sls.info(f'{prefix}/mysql', '接收参数',
                 db_name=req.db_name, sql=req.sql, args=req.args)
    res = logic.execute_mysql(req.sql, req.args, db_name=req.db_name)
    return res
