import requests
import re
import csv
import time
from pathlib import Path

BASE_URL = 'https://movie.douban.com/top250'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'
}
FILE_PATH = Path(__file__).parent / 'top250.csv'

regex = re.compile(
    # r"""
    # <span\ class="title">(?P<name>.*?)</span>.*?
    # 导演:\ (?P<director>.*?)(?:&nbsp;.*?)?
    # <br>(?P<year>.*?)&nbsp;.*?
    # <span\ class="rating_num"\ property="v:average">(?P<score>.*?)</span>.*?
    # <span>(?P<num>.*?)人评价</span>
    # """,
    r'<span class="title">(?P<name>.*?)</span>.*?'
    r'<p>.*?导演: (?P<director>.*?)(?:&nbsp;.*?)?'
    r'<br>(?P<year>.*?)&nbsp;.*?'
    r'<span class="rating_num" property="v:average">(?P<score>.*?)</span>.*?'
    r'<span>(?P<num>.*?)人评价</span>',
    re.S,
)


def fetch_page(session, start):
    url = f'{BASE_URL}?start={start}'
    resp = session.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.text


def parse_movies(html):
    for item in regex.finditer(html):
        yield [
            item.group('name'),
            item.group('director'),
            item.group('year').strip(),
            item.group('score'),
            item.group('num'),
        ]


def save_csv(rows):
    with open(FILE_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(['电影名', '导演', '年份', '评分', '评价人数'])

        for row in rows:
            writer.writerow(row)


def main():
    all_movies = []

    with requests.Session() as session:
        for start in range(0, 250, 25):
            print(f'正在抓取 start={start}')

            html = fetch_page(session, start)

            for movie in parse_movies(html):
                # print(movie)
                all_movies.append(movie)

            time.sleep(1)

    save_csv(all_movies)
    print('完成')


if __name__ == '__main__':
    main()
