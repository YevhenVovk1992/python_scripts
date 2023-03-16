import datetime
import os

import aiohttp
import asyncio
import pandas as pd

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


async def parser_main_page(link):
    """
    Parse page
    :param link:
    :return:
    """
    all_companies = []
    page = await get_page(link)
    if page:
        soup = BeautifulSoup(page, 'html.parser')
        sections = soup.find_all('div', class_='funds-list-item w-dyn-item')
        print('Get links to pages of companies')

        for el in sections:
            try:
                name = el.find('a').text
                link = el.find('a').get('href')
                data = el.find('div', class_='investor-box-right')
                subscription_amount = data.find('div', class_='value funds-value value-b_a').text + data.find('div', class_='value funds-value').text
                Subscription_Period = el.find('div', class_='rf-top-items').find_all('div', class_='value funds-value')[1].text
                carry = el.find('div', class_='rf-bottom-items').find_all('div', class_='value funds-value')[0].text
                Mgmt_Fee = el.find('div', class_='rf-bottom-items').find_all('div', class_='value funds-value')[1].text
                Other_Fees = el.find('div', class_='rf-bottom-items').find_all('div', class_='value funds-value')[2].text
            except:
                pass
            else:
                all_companies.append(
                    (name, link, subscription_amount, Subscription_Period, carry, Mgmt_Fee, Other_Fees)
                )
    return all_companies


async def save_to_file(company_list: list):
    """
    Save data to file
    :param company_list: data list
    :return: None
    """
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list6 = []
    list7 = []
    for x in company_list:
        list1.append(x[0])
        list2.append(x[1])
        list3.append(x[2])
        list4.append(x[3])
        list5.append(x[4])
        list6.append(x[5])
        list7.append(x[6])
    data = pd.DataFrame({
        'name': list1,
        'link': list2,
        'subscription_amount': list3,
        'Subscription_Period': list4,
        'carry': list5,
        'Mgmt_Fee': list6,
        'Other_Fees': list7
    })
    now_date = datetime.date.today()
    file_path = os.path.join(os.path.dirname(__file__), f'{now_date}-angellist.xlsx')
    print('Save file')
    data.to_excel(file_path, sheet_name='sheet1', index=False)


async def controller_venture() -> None:
    print("Start venture parser")
    main_link = "https://www.angellist.com/rolling"
    link_list = await parser_main_page(main_link)
    await save_to_file(link_list)
    print("End venture parser")


async def main():
    await controller_venture()


if __name__ == "__main__":
    asyncio.run(main())
