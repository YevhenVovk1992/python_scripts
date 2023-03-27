import os
import time

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '6297758340:AAHPidGXBR4IBS4ooji9O2eFocJLdIXviAM'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Get news', callback_data='/get_news'))
    markup.add(types.InlineKeyboardButton('Go to site', url='https://www.tesmanian.com/blogs/tesmanian-blog'))
    await message.reply("Привет!", reply_markup=markup)


@dp.message_handler(commands=['get_news'])
async def get_news(message: types.Message):
    SV_table_path = os.path.abspath(os.path.dirname(__file__)) + '/tesmanian.csv'
    article_array = {}

    with open(SV_table_path, 'r') as file:
        for row in file:
            article = row.split(';')
            article_array[article[0]] = article[1]

    while True:
        with open(SV_table_path, 'r') as file:
            for row in file:
                article = row.split(';')
                if article[0] in article_array:
                    print('Bot sleep')
                    time.sleep(20)
                    continue
                else:
                    print('send ne article')
                    article_array[article[0]] = article[1]
                    await message.answer(f'{article[0]}\n{article[1]}')
        print('start loop again')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)