#!-*- coding:utf-8 -*-
# FileName:

from fastapi import APIRouter
from pydantic import BaseModel

from module.browser import logic
from utils import log_sls

prefix = 'browser'
router = APIRouter(
    prefix=f'/{prefix}',
    tags=[prefix],
)


class Login(BaseModel):
    url: str
    email: str
    password: str


@router.post("/google_login")
async def google_login(req: Login):
    log_sls.info(f'{prefix}/google_login', '接收参数', url=req.url, email=req.email)
    return logic.google_login(req.url, email=req.email, password=req.password)


@router.get("/html")
async def get_html(
        url: str,
):
    log_sls.info(f'{prefix}/html', '接收参数', url=url)
    return logic.get_html(url)
