import requests
import json
from db import *
from utils import get_usd_eur


def get_stock_data(assets):
    exchange_rate = get_usd_eur()

    def convert_usd_to_eur(data, exchange_rate):
        convert_fields = ['regularMarketPrice', 'regularMarketOpen', 'trailingAnnualDividendYield']

        for symbol in data:
            if 'currency' in symbol and symbol['currency'] == 'USD':
                for field in convert_fields:
                    if field in symbol:
                        symbol[field] = float(symbol[field]) * exchange_rate

        return data

    api = 'https://query1.finance.yahoo.com/v7/finance/quote?'

    symbols = [symbol['symbol'] for symbol in assets if symbol['symbol'] is not None]
    symbols = 'symbols=' + ','.join(symbols)

    req = requests.get(api + symbols).json()

    data = req['quoteResponse']['result']
    data = convert_usd_to_eur(data, exchange_rate)

    return data


def check_if_asset_symbol_exists(symbol):
    api = 'https://query1.finance.yahoo.com/v7/finance/quote?symbols={}'.format(symbol)

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

    return assets


def update_assets(conn):
    assets = select_all_symbols(conn)
    assets = prepare_assets(assets, conn)
    update_all_assets(conn, assets)
