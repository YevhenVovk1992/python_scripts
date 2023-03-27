from parser_tesmanian import loop_news
from bot import executor, dp
from multiprocessing import Process


def start_bot():
    executor.start_polling(dp, skip_updates=True)


def start_parser():
    loop_news()


def main():
    process_1 = Process(target=start_parser)
    process_2 = Process(target=start_bot)
    process_1.start()
    process_2.start()


if __name__ == "__main__":
    main()
