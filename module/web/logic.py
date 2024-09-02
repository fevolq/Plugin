from typing import List

from module.web import search, parse


async def web_search(q, num: int, prefix_url: str):
    urls = await search.fetch_from_google(q, num=num, check_prefix=prefix_url)
    if not urls:
        urls = await search.fetch_from_google_sdk(q, num=num, check_prefix=prefix_url)
    return {
        'code': 200,
        'data': urls
    }


async def parse_html(
        url,
        *,
        max_length: int = -1,
        timeout: int = -1,
        retry: int = 0,
        xpath: str='//*',
        remove_xpath: List[str] = None,
        headers: dict = None,
):
    content, html = await parse.parse_url_2_md(url=url, timeout=timeout, retry=retry,
                                               xpath=xpath, remove_xpath=remove_xpath,
                                               headers=headers)

    max_length = float('inf') if max_length < 0 else int(max_length)
    return {
        'content': content[:max_length] if max_length != float('inf') else content,
        'html': html,
    }
