from typing import List

from module.send import feishu


def feishu_robot_text(url: str, text: str, *, title: str = None, href: List[dict] = None, at: str = None):
    res = feishu.robot_text(url, text, title=title, href=href, at=at)
    return {
        'code': 200 if res.json()['code'] == 0 else 400,
        'msg': res.json()['msg'],
    }


def feishu_robot_text_v2(url: str, content: List[List[dict]], *, title: str = None):
    res = feishu.robot_text_v2(url, content, title=title)
    return {
        'code': 200 if res.json()['code'] == 0 else 400,
        'msg': res.json()['msg'],
    }


def feishu_robot_template(url: str, template_id: str, version: str, variable: dict):
    res = feishu.robot_template(url, template_id, version, variable=variable)
    return {
        'code': 200 if res.json()['code'] == 0 else 400,
        'msg': res.json()['msg'],
    }
