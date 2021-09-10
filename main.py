from datetime import datetime
from dateutil.relativedelta import relativedelta

import configparser
import csv
import logging
import yfinance as yf


CONFIG = configparser.ConfigParser()
CONFIG.read('config/local.ini')
CRYPTO_LIST_PATH = CONFIG.get('CRYPTO', 'LIST_PATH')
FILE_ENCODING = CONFIG.get('FILE', 'ENCODING')
LOGGING_MAIN_PATH = CONFIG.get('LOGGING', 'MAIN_PATH')
MAIN_GET_MAX_NUMBER_OF_YEAR_DATA = CONFIG.get('MAIN', 'GET_MAX_NUMBER_OF_YEAR_DATA')
SPX_CONSTITUENTS_PATH = CONFIG.get('SPX', 'CONSTITUENTS_PATH')
CRYPTO_PATH = CONFIG.get('CRYPTO', 'PATH')


def fetch_cryptos_price():
    """Return nothing."""
    today = datetime.today().strftime('%Y-%m-%d')
    pass_years = datetime.now() - relativedelta(years=int(MAIN_GET_MAX_NUMBER_OF_YEAR_DATA))
    pass_years = pass_years.strftime('%Y-%m-%d')

    with open(CRYPTO_LIST_PATH, newline='', encoding=FILE_ENCODING) as file:
        crypto_list = csv.reader(file)
        next(crypto_list)
        for crypto in crypto_list:
            stock = crypto[0].replace(".", "-")
            data = yf.download(stock, pass_years, today)
            data.to_csv(CRYPTO_PATH + crypto[0] + ".csv")
            print("Downloaded {} data".format(crypto[0]))
            logging.info("Downloaded %s data", crypto[0])


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M',
        handlers=[logging.FileHandler(LOGGING_MAIN_PATH, 'w', 'utf-8'), ]
    )
    fetch_cryptos_price()


if __name__ == "__main__":
    main()
