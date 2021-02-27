import requests
import json
from mysql import *


def get_stock_data(assets):
    api = 'https://query1.finance.yahoo.com/v7/finance/quote?'

    symbols = [symbol['symbol'] for symbol in assets if symbol['symbol'] is not None]
    symbols = 'symbols=' + ','.join(symbols)

    # print(api + symbols)

    req = requests.get(api + symbols)
    return req.json()['quoteResponse']['result']


def calc_asset_value(quantity, price):
    return round(quantity * price, 2)


def calc_asset_profit(value, quantity, buyin, price_open):
    profit_total_absolute = round(value - (quantity * buyin), 2)

    profit_today_absolute = round(value - (quantity * price_open), 2)

    return profit_total_absolute, profit_today_absolute


def calc_asset_dividend(dividended_rate, dividended_yield, quantity):
    dividended_rate = float(dividended_rate)
    dividended_yield = float(dividended_yield * 100)
    my_dividend = dividended_rate * quantity

    return dividended_rate, dividended_yield, my_dividend


def prepare_assets(assets):
    data = get_stock_data(assets)

    for i in range(len(data)):
        quantity = assets[i]['quantity']
        buyin = assets[i]['buyin']
        price = data[i]['regularMarketPrice']
        priceOpen = data[i]['regularMarketOpen']

        value = calc_asset_value(quantity, price)

        profit_total, profit_today = calc_asset_profit(value, quantity, buyin, priceOpen)

        assets[i]['price'] = price
        assets[i]['priceOpen'] = priceOpen
        assets[i]['value'] = value
        assets[i]['profit_total'] = profit_total
        assets[i]['profit_today'] = profit_today

        # only for stocks
        if 'trailingAnnualDividendRate' in data[i]:
            dividended_rate, dividended_yield, my_dividend = calc_asset_dividend(data[i]['trailingAnnualDividendRate'],
                                                                                 data[i]['trailingAnnualDividendYield'],
                                                                                 quantity)
            assets[i]['dividendedRate'] = dividended_rate
            assets[i]['dividendedYield'] = dividended_yield
            assets[i]['myDividend'] = my_dividend

    return assets
