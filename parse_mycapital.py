import pandas as pd
import datetime
import os.path
import time
import aiohttp
import asyncio

from bs4 import BeautifulSoup


async def get_page(link: str) -> str:
    """
    Get all link on the page
    :param link: str
    :return: html
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(link) as resp:
            if resp.status == 200:
                return await resp.text()
            print("No connect to {}".format(link))


async def get_links_from_page(html_page: str) -> list:
    """
    Get all links from page
    :param html_page: link to page
    :return: list of links
    """
    link_list = []
    try:
        soup = BeautifulSoup(html_page, 'html.parser')
    except TypeError:
        pass
    else:
        for link in soup.find_all('div', class_='elementor-post__text'):
            page = link.find('a')
            link_list.append(page.get('href'))
    return link_list


async def get_count_pages(html_page: str) -> int:
    """
    Get the number of pages in the paginator
    :param html_page: first page
    :return: number of pages
    """
    try:
        soup = BeautifulSoup(html_page, 'html.parser')
    except TypeError:
        pass
    else:
        paginator = soup.find('nav', class_='elementor-pagination')
        number_of_pages = len(paginator.find_all('a')) + 1
        return number_of_pages


async def parse_page(http_link: str) -> tuple:
    """
    Get page and parse data from it
    :param http_link: link to the company page
    :return: tuple
    """
    company = None
    page = await get_page(http_link)
    if page:
        soup = BeautifulSoup(page, 'html.parser')
        name = soup.find('section', {"data-id": "85d4596"}).text
        country = soup.find('section', {"data-id": "540c2a5"}).text
        email = soup.find('section', {"data-id": "0c879f4"}).text
        company = (name.strip(), country.strip(), email.strip())
    return company


async def get_all_links(link: str, number_page: int) -> list:
    """
    Accept a link to the page and a page number. Get links to companies from this page
    :param link: link to first page
    :param number_page: number of the page
    :return:
    """
    page = await get_page(link + 'page/{}/'.format(number_page))
    print('Get links from {} page'.format(number_page))
    links = await get_links_from_page(page)
    return links


async def save_to_file(data_list: list) -> None:
    """
    Save data to csv table
    :param data_list: data in format: Name, Country, email
    :return: None
    """
    list1 = []
    list2 = []
    list3 = []
    now_date = datetime.date.today()
    file_path = os.path.join(os.path.dirname(__file__), f'{now_date}-mycapital.xlsx')
    for string in data_list:
        x = await string
        list1.append(x[0])
        list2.append(x[1])
        list3.append(x[2])
    data = pd.DataFrame({
        'name': list1,
        'Country': list2,
        'email': list3
    })
    data.to_excel(file_path, sheet_name='sheet1', index=False)


async def controller_mycapital(requests_per_minute: int, sleep_time_after_100_requests: int) -> None:
    """
    Run parser
    :param requests_per_minute: int
    :param sleep_time_after_100_requests: int
    :return: None
    """
    tasks = []
    link_list = []
    main_link = "https://www.mycapital.com/angel-investor/"
    pages = await get_count_pages(await get_page(main_link))

    # Get all links from all pages
    n = 1
    while n <= pages:
        task = asyncio.create_task(get_all_links(main_link, n))
        tasks.append(task)
        n += 1
    await asyncio.gather(*tasks)
    for lst in tasks:
        link_list.extend(await lst)
    tasks.clear()

    # Parse pages
    for i, link in enumerate(link_list):
        print('Send request to {}'.format(link))
        task1 = asyncio.create_task(parse_page(link))
        tasks.append(task1)
        time.sleep(60/requests_per_minute)
        if i != 0 and i % 100 == 0:
            print('---WAIT!---')
            await asyncio.gather(*tasks)
            time.sleep(sleep_time_after_100_requests)

    # Save to the file
    await save_to_file(tasks)
    print()
    print('End mycapital parser')


async def main():
    await controller_mycapital()


if __name__ == "__main__":
    asyncio.run(main())
