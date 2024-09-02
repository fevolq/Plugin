from typing import List

from fastapi import APIRouter, Query
from pydantic import BaseModel

from module.send import logic
from utils import log_sls

prefix = 'send'
router = APIRouter(
    prefix=f'/{prefix}',
    tags=[prefix],
)


class FeiShuText(BaseModel):
    url: str = Query(description='机器人链接')
    text: str = Query(description='文本内容')
    title: str = Query(default=None, description='标题')
    href: List[dict] = Query(default=None, description='超链接 {href: ..., text: ...}')
    at: str = Query(default=None, description='@user_id')


@router.post('/feishu/text', description='发送飞书文本消息（简略版）')
async def send_feishu_text(req: FeiShuText):
    log_sls.info(f'{prefix}/feishu/text', '接收参数',
                 url=req.url, title=req.title, )
    res = logic.feishu_robot_text(req.url, req.text, title=req.title, href=req.href, at=req.at)
    return res


class FeiShuTextV2(BaseModel):
    url: str = Query(description='机器人链接')
    title: str = Query(default=None, description='标题')
    content: List[List[dict]] = Query(description='content内容')


@router.post('/feishu/text/v2', description='发送飞书文本消息')
async def send_feishu_text_v2(req: FeiShuTextV2):
    log_sls.info(f'{prefix}/feishu/text/v2', '接收参数',
                 url=req.url, title=req.title, )
    res = logic.feishu_robot_text_v2(req.url, req.content, title=req.title)
    return res


class FeiShuTemplate(BaseModel):
    url: str = Query(description='机器人链接')
    templateID: str = Query(description='模板ID')
    version: str = Query(description='模板版本')
    variable: dict = Query(description='参数')


@router.post('/feishu/template', description='发送飞书模板消息')
async def send_feishu_template(req: FeiShuTemplate):
    log_sls.info(f'{prefix}/feishu/template', '接收参数',
                 url=req.url, templateID=req.templateID, version=req.version)
    res = logic.feishu_robot_template(req.url, req.templateID, req.version, req.variable)
    return res
