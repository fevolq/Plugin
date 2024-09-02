from typing import List

from fastapi import APIRouter, Query
from pydantic import BaseModel

from module.web import logic
from utils import log_sls

prefix = 'web'
router = APIRouter(
    prefix=f'/{prefix}',
    tags=[prefix],
)


@router.get("/search")
async def web_search(q: str, num: int = 3, prefix_url: str = None):
    """根据关键字，查找对应的链接"""
    log_sls.info(f'{prefix}/search', '接收参数', q=q, num=num, prefix_url=prefix_url)
    if prefix_url is None:  # 为''时，则不校验url的有效性
        prefix_url = 'https://r.jina.ai/'
    num = max(num, 1)
    res = await logic.web_search(q, num=int(num), prefix_url=prefix_url)
    return res


class Parse(BaseModel):
    url: str
    max_length: int = -1
    timeout: int = Query(3000, description='超时时间（ms）')
    retry: int = Query(0, description='重试次数', ge=0)
    xpath: str = Query('//*', description='xpath选择器（需要的html节点）')
    remove_xpath: List[str] = Query([], description='xpath选择器（移除的html节点）')
    headers: dict = Query(None, description='额外的headers')


@router.post("/parse", description='解析链接内容')
async def parse_html(req: Parse):
    """解析链接内容"""
    log_sls.info(f'{prefix}/parse', '接收参数',
                 url=req.url, max_length=req.max_length, timeout=req.timeout, retry=req.retry,
                 xpath=req.xpath, remove_xpath=req.remove_xpath, headers=req.headers)
    res = await logic.parse_html(req.url, max_length=req.max_length, timeout=req.timeout, retry=req.retry,
                                 xpath=req.xpath, remove_xpath=req.remove_xpath, headers=req.headers)
    return res
