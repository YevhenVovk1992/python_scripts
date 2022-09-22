"""
    Parser auto.ria.com

    The parser receives a new car catalog with a link, price, region.
    After. writes to a file with the .CSV extension and automatically opens it.
"""
import os
import sys
import subprocess

import requests
import csv

from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool

URL = str()
ALL_MODELS_URL = 'https://auto.ria.com/uk/newauto/catalog/'
HOST = 'https://auto.ria.com/uk'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'accept': '*/*'
}


def get_html(url: str, params=None) -> requests.models.Response:
    req = requests.get(url, headers=HEADERS, params=params)
    return req


def get_all_models() -> None:
    models = []
    soup = BeautifulSoup(get_html(ALL_MODELS_URL).text, 'html.parser')
    items = soup.find_all('a', class_='item-brands')
    for item in items:
        m = item.get_text().strip()
        models.append(m.split(' ')[0].lower())
    print('\tWhat car model are you interested in?')
    for i, car in enumerate(models):
        if i%10 == 0:
            print()
        print(car, end=' ')
    print('\n')


def get_pages_count(html: str) -> int:
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='page-item mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


def get_content(html: str) -> list:
    cars = []
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='proposition_link')
    for item in items:
        cars.append({
            'title': item.find('div', class_='proposition_title').text.strip(),
            'link': HOST + item.get('href'),
            'price': item.find('span', class_='green bold size22').text.strip(),
            'city': item.find('span', class_='item region').get_text(strip=True)
        })
    return cars


def parse() -> list:
    all_cars = []
    html = get_html(URL)
    if html.status_code == 200:
        pages = get_pages_count(html.text)
        links = list(f'{URL}?page={page}' for page in range(1, pages + 1))
        pool = ThreadPool(pages)
        pool.map(lambda link: all_cars.extend(get_content(get_html(link).text)), links)
        pool.close()
        pool.join()
        print(f'We have got {len(all_cars)} cars.')
    else:
        print('Page not found')
    return all_cars


def write_file(data: list, model: str) -> None:
    with open(f'{model}_from_autoria.cvs', 'w') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Title', 'Link', 'Price', 'City'])
        for el in data:
            writer.writerow([el['title'], el['link'], el['price'], el['city']])


def open_file(filename: str) -> None:
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


def main():
    global URL
    get_all_models()
    model = input("Input model: ").lower().strip()
    URL = f'https://auto.ria.com/uk/newauto/marka-{model}/'
    data = parse()
    write_file(data, model)
    open_file(f'{model}_from_autoria.cvs')


if __name__ == '__main__':
    main()
