import csv
import os
import time

from requests_html import HTMLSession
from bs4 import BeautifulSoup

DOMAIN = 'www.tesmanian.com'
URL_BLOG = 'https://www.tesmanian.com/blogs/tesmanian-blog'


class GetNews:
    def __init__(self):
        self.session = HTMLSession()
        self.news_array = {}

    def get_page(self, url):
        r = self.session.get(url)
        if r.status_code == 200:
            r.html.render(sleep=1, keep_page=True, scrolldown=1)
            html_page = r.text
            return html_page

    def _reload_session(self):
        self.session.close()
        self.session = HTMLSession()

    def _get_paginator(self, html_page):
        soup = BeautifulSoup(html_page, 'html.parser')
        how_many_page = soup.find('span', class_='pagination__current')
        paginator_range = int(how_many_page.text.split('/')[1])
        return paginator_range

    def _parse_page(self, html_page, domain, presence_check=False):
        new_title = {}
        soup = BeautifulSoup(html_page, 'html.parser')
        links = soup.find_all('blog-post-card')
        for ln in links:
            name = ln.find('p').text.strip()
            href = ln.find('a')['href'].strip()
            if presence_check:
                if name in self.news_array:
                    continue
                else:
                    new_title[name] = domain + href
            print('Add the article - ', name)
            self.news_array[name] = domain + href
        if new_title:
            return new_title

    def _get_page_and_parse(self, url, domain, presence_check=False):
        success = 0
        titles = None
        while success < 3:
            try:
                first_page = self.get_page(url)
            except Exception:
                success += 1
                print('Try get page again: 1')
                self._reload_session()
                continue
            else:
                titles = self._parse_page(first_page, domain, presence_check=presence_check)
                success += 3
        return titles

    def get_all_news(self, url, domain, paginator_page=None):
        paginator = '?page='
        first_page = self.get_page(url)
        max_paginator_page = paginator_page if paginator_page is not None else self._get_paginator(first_page)
        for page in range(max_paginator_page, 0, -1):
            print('Get page: ', page)
            self._get_page_and_parse(url + paginator + str(page), domain)
        return self.news_array

    def save_to_csv(self, path, write_method='w'):
        with open(path, write_method) as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['title', 'link'])
            for title, link in self.news_array.items():
                writer.writerow([title, link])
        print('File save success')

    def update_buffer_from_file(self, path):
        with open(path, 'r') as file:
            for i, row in enumerate(file):
                if i == 0:
                    continue
                title = row.split(';')[0]
                link = row.split(';')[1]
                self.news_array[title] = link

    def write_latest_news_task(self, url, domain, path):
        print('Check a new article...')
        titles_are_exist = self._get_page_and_parse(url, domain, presence_check=True)
        if titles_are_exist:
            with open(path, 'a') as file:
                writer = csv.writer(file, delimiter=';')
                for title, link in titles_are_exist.items():
                    writer.writerow([title, link])
            print('File save success')


def loop_news():
    CSV_table_path = os.path.abspath(os.path.dirname(__file__)) + '/tesmanian.csv'
    parser = GetNews()
    if not os.path.exists(CSV_table_path):
        print('Create CSV table')
        parser.get_all_news(URL_BLOG, DOMAIN)
        parser.save_to_csv(CSV_table_path)
    parser.update_buffer_from_file(CSV_table_path)
    while True:
        parser.write_latest_news_task(URL_BLOG, DOMAIN, CSV_table_path)
        time.sleep(15)


def main():
    loop_news()


if __name__ == "__main__":
    main()
