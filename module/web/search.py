import requests
from bs4 import BeautifulSoup
from googlesearch import search  # pip install google

from utils import pools


async def fetch_from_google(keyword, *, num: int, check_prefix: str = '') -> list:
    try:
        url = f"https://www.google.com.hk/search?q={keyword}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find_all('a', class_='cz3goc BmP5tf')

        urls = []
        for i, item in enumerate(search_results):
            link = item.get('href', '')
            urls.append(link)
            if link not in urls:
                urls.append(link)
            if len(urls) == num:
                break

        def check_available(base_url) -> bool:
            check_link = f'{check_prefix}{base_url}'
            return url_is_available(check_link)

        result = []
        if check_prefix and urls:
            args_list = [[(item,)] for item in urls]
            available_res = pools.execute_thread(check_available, args_list=args_list, pools=len(args_list),
                                                 force_pool=True)
            for index, item in enumerate(urls):
                if not available_res[index]:
                    continue
                result.append(item)

        return result or urls
    except Exception as e:
        return []


async def fetch_from_google_sdk(keyword, *, num: int, check_prefix: str = ''):
    times = 0
    data = set()
    while times < 5 and len(data) < num:
        times += 1
        resp = search(keyword, num=num * 2, start=num * 2 * times, stop=num * 2 * (times + 1))

        for item in resp:
            if check_prefix:
                check_link = f'{check_prefix}{item}'
                if not url_is_available(check_link):
                    continue
            data.add(item)
    return list(data)[:num]


def url_is_available(url) -> bool:
    resp = requests.get(url)
    return resp.status_code == 200
