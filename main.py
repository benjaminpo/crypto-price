from datetime import datetime
from dateutil.relativedelta import relativedelta

import configparser
import csv
import logging
import yfinance as yf

CONFIG = configparser.ConfigParser()
CONFIG.read('config/local.ini')


def fetch_cryptos_price():
    """Return nothing."""

    CRYPTO_LIST_PATH = CONFIG.get('CRYPTO', 'LIST_PATH')
    FILE_ENCODING = CONFIG.get('FILE', 'ENCODING')
    MAIN_GET_MAX_NUMBER_OF_YEAR_DATA = CONFIG.get('MAIN', 'GET_MAX_NUMBER_OF_YEAR_DATA')
    CRYPTO_PATH = CONFIG.get('CRYPTO', 'PATH')

    pass_years = datetime.now() - relativedelta(years=int(MAIN_GET_MAX_NUMBER_OF_YEAR_DATA))
    pass_years = pass_years.strftime('%Y-%m-%d')
    ticker_list = []
    with open(CRYPTO_LIST_PATH, newline='', encoding=FILE_ENCODING) as file:
        list = csv.reader(file)
        next(list)
        for ticker in list:
            ticker_list.append(ticker[0].replace(".", "-"))
    data = yf.download(
        tickers=ticker_list,
        period=MAIN_GET_MAX_NUMBER_OF_YEAR_DATA + 'y',
        interval='1d',
        group_by='ticker',
        auto_adjust=False,
        prepost=False,
        threads=True,
        proxy=None
    )
    data = data.T
    for ticker in ticker_list:
        data.loc[(ticker,), ].T.to_csv(CRYPTO_PATH + ticker + '.csv', sep=',', encoding='utf-8')


def main():
    LOGGING_MAIN_PATH = CONFIG.get('LOGGING', 'MAIN_PATH')
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M',
        handlers=[logging.FileHandler(LOGGING_MAIN_PATH, 'w', 'utf-8'), ]
    )
    fetch_cryptos_price()


if __name__ == "__main__":
    main()
