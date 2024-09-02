import base


def web_search():
    params = dict(
        q='武汉天气',
        prefix_url='',
        num=5,
    )
    res = base.request('GET', 'web/search', params=params)
    print(res.json())


def web_parse():
    params = dict(
        url='https://app.diandian.com/app/xoupuzpxq6172al/ios-rank?market=1&country=125&id=6446141770',
        timeout=-1,
        retry=1,
        xpath='//*[@class="rank-table"]',
        remove_xpath=[],
    )
    res = base.request('POST', 'web/parse', json=params)
    print(res.json())


if __name__ == '__main__':
    ...
    # web_search()
    # web_parse()
