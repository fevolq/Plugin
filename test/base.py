import requests

import config


server = f'127.0.0.1/{config.PORT}'


def request(method, end_point, **kwargs):
    url = f'http://{server}/{end_point}'
    resp = requests.request(method=method, url=url, **kwargs)
    print(resp.status_code)
    return resp
