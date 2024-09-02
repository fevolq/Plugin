import base


def google_login():
    end_point = 'browser/google_login'
    params = {
        'url': '',
        'email': '',
        'password': ''
    }
    res = base.request('post', end_point, json=params)
    print(res.json())


def html():
    end_point = 'browser/html'
    params = {
        'url': 'https://www.google.com',
    }
    res = base.request('get', end_point, params=params)
    print(res.json())


if __name__ == '__main__':
    ...
    # google_login()
    # html()
