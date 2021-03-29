import requests
import json
from db import *


def get_stock_data(assets):
    api = 'https://query1.finance.yahoo.com/v7/finance/quote?'

    symbols = [symbol['symbol'] for symbol in assets if symbol['symbol'] is not None]
    symbols = 'symbols=' + ','.join(symbols)

    print(api + symbols)

    req = requests.get(api + symbols)
    return req.json()['quoteResponse']['result']


def check_if_asset_symbol_exists(symbol):
    api = 'https://query1.finance.yahoo.com/v7/finance/quote?symbols={}'.format(symbol)

    print(api)

    req = requests.get(api).json()
    result = req['quoteResponse']['result']

    if result is None or len(result) == 0:
        return False

    return True


def calc_asset_dividend(dividended_rate, dividended_yield, quantity):
    dividended_rate = float(dividended_rate)
    dividended_yield = float(dividended_yield * 100)
    my_dividend = dividended_rate * quantity

    return dividended_rate, dividended_yield, my_dividend


def prepare_assets(assets, conn):
    data = get_stock_data(assets)


    for i in range(len(data)):
        price = data[i]['regularMarketPrice']
        priceOpen = data[i]['regularMarketOpen']

        dividended_rate, dividended_yield, my_dividend = 0, 0, 0
        if 'trailingAnnualDividendRate' in data[i]:
            dividended_rate, dividended_yield, my_dividend = calc_asset_dividend(data[i]['trailingAnnualDividendRate'],
                                                                                 data[i]['trailingAnnualDividendYield'],
                                                                                 1)

        assets[i]['regularMarketPrice'] = price
        assets[i]['regularMarketOpen'] = priceOpen

        assets[i]['trailingAnnualDividendRate'] = dividended_rate
        assets[i]['trailingAnnualDividendYield'] = dividended_yield
        assets[i]['dividend'] = my_dividend

        print(data)
        print('prepare_assets: ', assets[i]['symbol'], data[i]['symbol'])

    return assets


def update_assets(conn):
    assets = select_all_symbols(conn)
    assets = prepare_assets(assets, conn)
    update_all_assets(conn, assets)
