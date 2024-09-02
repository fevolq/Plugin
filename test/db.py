import base

def redis():
    end_point = 'db/redis'
    params = {}
    # string
    # params = {
    #     'action': 'set',
    #     'db_name': 0,
    #     'args': ['test:string', 'test']
    # }
    # params = {
    #     'action': 'get',
    #     'db_name': 0,
    #     'args': ['test:string']
    # }

    # # hash
    # params = {
    #     'action': 'hmset',
    #     'db_name': 0,
    #     'args': ['test:hash', {'a': 1, 'b': 2, 'c': 'cc'}]
    # }
    # params = {
    #     'action': 'hgetall',
    #     'db_name': 0,
    #     'args': ['test:hash']
    # }
    res = base.request('post', end_point, json=params)
    print(res.json())


def mysql():
    end_point = 'db/mysql'
    params = {
        # 'db_name': '',

        # 'sql': 'show databases',
        'sql': 'SELECT * FROM `test`',
        # 'sql': 'INSERT `test` (name) VALUES ("demo")',
    }
    res = base.request('post', end_point, json=params)
    print(res.json())


if __name__ == '__main__':
    ...
    # redis()
    # mysql()
