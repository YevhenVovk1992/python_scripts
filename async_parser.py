import os
from configparser import ConfigParser
import asyncio


from parse_venture import controller_venture
from parse_mycapital import controller_mycapital


async def main():
    """
    Run moduls
    :return: None
    """
    #Get the configparser object
    
    config_object = ConfigParser()
    config_ini_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    if not os.path.exists(config_ini_path):
        with open('config.ini', 'w') as conf:
            config_object["PARSER"] = {
                "requests_per_minute": "100",
                "sleep_time_after_100_requests": "60"
            }
            config_object.write(conf)
    else:
        config_object.read("config.ini")

    requests_per_minute = int(config_object['PARSER']['requests_per_minute'])
    sleep_time_after_100_requests = int(config_object['PARSER']['requests_per_minute'])

    await controller_venture()
    await controller_mycapital(requests_per_minute, sleep_time_after_100_requests)
    print('Operation successful')


if __name__ == "__main__":
    asyncio.run(main())

