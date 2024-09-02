import re
from typing import List

from playwright.async_api import async_playwright
from markdownify import markdownify as md
from lxml import etree

from utils import log_sls


async def get_html(url, *, headers: dict = None, timeout=-1, retry=0) -> str:
    timeout = timeout if timeout > 0 else None
    headers = headers or {}
    while retry >= 0:
        try:
            async with async_playwright() as p:
                browser_type = p.chromium
                browser = await browser_type.launch()
                page = await browser.new_page()
                await page.set_extra_http_headers(headers)
                await page.goto(url, timeout=timeout)
                await page.wait_for_load_state('networkidle')
                # text = await page.inner_html(xpath)
                text = await page.content()
                await browser.close()
                break
        except Exception as e:
            log_sls.error('parse', 'url请求异常', url=url, timeout=timeout)
            retry -= 1
            if retry < 0:
                raise Exception('链接解析失败')
            else:
                log_sls.info('parse', '重试下一次', retry=retry + 1)
    return text


def load_etree(html: str, xpath: str, remove_xpath: [str]) -> (str, str):
    """
    解析html，获取指定的xpath节点，并移除指定的xpath节点
    :param html:
    :param xpath:
    :param remove_xpath:
    :return: 文本内容、html
    """
    htmls = etree.HTML(html).xpath(xpath)
    res_html = []
    res_text = []
    for item_html in htmls:
        for remove_x in remove_xpath:
            ele_remove = item_html.xpath(remove_x)
            for ele in ele_remove:
                ele.getparent().remove(ele)

        item_html_str = etree.tostring(item_html, encoding='utf-8').decode('utf-8')
        res_html.append(item_html_str)

        item_html = etree.HTML(item_html_str)  # 需要将移除xpath后的html重新构建。如果直接使用item_html，会出现未知情况（直接使用了全部的html？）
        text = item_html.xpath('//text()')
        res_text.append('\n\n'.join(item for item in text if item.strip(' ').strip('\n')))

    return '\n'.join(res_text), '\n\n'.join(res_html)


def replace_multiple_newlines_with_single(content):
    # 使用正则表达式替换两个或以上连续的换行符为单个换行符
    content = re.sub(r'\n+', '\n', content)
    content = re.sub(r'\r+', '\r', content)
    content = re.sub(r'\t+', '\t', content)
    return content


async def parse_url_2_md(*, url='', html='', timeout=-1, retry=0,
                         xpath='//*', remove_xpath: List[str] = None,
                         headers: dict = None) -> (str, str):
    """
    提取html内容
    :param url:
    :param html:
    :param timeout:
    :param retry:
    :param xpath:
    :param remove_xpath:
    :param headers:
    :return:
    """
    assert any([url, html]), 'url、html 必填一个'
    retry = max(retry, 0)
    headers = headers or {}

    text = ''
    if url:
        html = await get_html(url, timeout=timeout, retry=retry, headers=headers)
    if html:
        text, html = load_etree(html, xpath=xpath, remove_xpath=remove_xpath or [])
    text = md(text)
    text = replace_multiple_newlines_with_single(text).strip('\n').strip('')
    return text, html


if __name__ == '__main__':
    import asyncio

    link = 'https://doc.fastgpt.in/docs/development/sealos/'

    asyncio.run(parse_url_2_md(url=link, xpath='//div[@id="content"]',
                               remove_xpath=['//*[@id="部署架构图"]', '//*[@id="多模型支持"]'],
                               headers={},
                               ))
