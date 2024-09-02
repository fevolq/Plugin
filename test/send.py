import base


def feishu_robot_text():
    end_point = 'send/feishu/text'
    params = {
        'url': '',
        'text': '测试',
        'title': '标题',
        'href': [
            {'href': 'https://www.baidu.com', 'text': '百度'},
            {'href': 'https://www.google.com', 'text': '谷歌'},
        ]
    }
    res = base.request('post', end_point, json=params)
    print(res.json())


def feishu_robot_text_v2():
    end_point = 'send/feishu/text/v2'
    params = {
        'url': '',
        'text': '测试',
        'title': '标题',
        'content': [
            [{'tag': 'text', 'text': '文本1'}, {'tag': 'text', 'text': ' '},
             {'tag': 'a', 'text': '飞书', 'href': 'https://open.feishu'}],
            [{'tag': 'text', 'text': '\n'}],
            [{'tag': 'text', 'text': '文本2'}, {'tag': 'text', 'text': '文本22'}, {'tag': 'text', 'text': '\n'},
             {'tag': 'a', 'text': '百度', 'href': 'https://www.baidu.com'}],
            [{'tag': 'text', 'text': '文本3'}, {'tag': 'a', 'text': 'google', 'href': 'https://www.google.com'}],
        ]
    }
    res = base.request('post', end_point, json=params)
    print(res.json())


def feishu_robot_template():
    end_point = 'send/feishu/template'
    params = {
        'url': '',
        'templateID': 'xxx',
        'version': '1.0.0',
        'variable': {

        }
    }
    res = base.request('post', end_point, json=params)
    print(res.json())


if __name__ == '__main__':
    ...
    # feishu_robot_text()
    # feishu_robot_text_v2()
    # feishu_robot_template()
