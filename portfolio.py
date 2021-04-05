import itertools
import operator

from db import *
from assets import *


def calc_asset_value(quantity, price):
    return round(quantity * price, 2)


def calc_asset_profit(value, quantity, buyin, price_open):
    profit_total_absolute = round(value - (quantity * buyin), 2)
    profit_today_absolute = round(value - (quantity * price_open), 2)

    profit_total_relative = round(profit_total_absolute / (value + 0.0000000001) * 100, 2)  # avoid division by zero
    profit_today_relative = round(profit_today_absolute / (value + 0.0000000001) * 100, 2)  # avoid division by zero
    return profit_total_absolute, profit_total_relative, profit_today_absolute, profit_today_relative


def calc_portfolio_value(portfolio_assets):
    return round(sum(asset['asset_value'] for asset in portfolio_assets), 2)


def calc_all_portfolios_value(portfolio_assets):
    return round(sum(asset['portfolio_value'] for asset in portfolio_assets), 2)


def calc_portfolio_profit(portfolio_assets):
    profit_total_absolute = round(sum(asset['profit_total_absolute'] for asset in portfolio_assets), 2)
    profit_today_absolute = round(sum(asset['profit_today_absolute'] for asset in portfolio_assets), 2)

    # function used for calculating value for one portfolio and all portfolios, todo
    if 'asset_value' in portfolio_assets[0]:
        value = sum(asset['asset_value'] for asset in portfolio_assets) + 0.0000000001  # avoid division by zero
    else:
        value = sum(asset['portfolio_value'] for asset in portfolio_assets if
                    asset['portfolio_type'] != 4) + 0.0000000001  # avoid division by zero

    profit_total_relative = round(profit_total_absolute / value * 100, 2)
    profit_today_relative = round(profit_today_absolute / value * 100, 2)

    return profit_total_absolute, profit_total_relative, profit_today_absolute, profit_today_relative


def calc_portfolio_dividend(portfolio_assets):
    dividend = round(sum(asset['dividend'] for asset in portfolio_assets), 2)

    return round(dividend, 2)


def calc_portfolio_percentage(portfolio_value, value):
    return round(value / portfolio_value * 100, 2)


def calc_sector_percentage(portfolio_data, portfolio_value, all_sectors):
    for sector in all_sectors:
        sector['value'] = round(
            sum(asset['asset_value'] for asset in portfolio_data if asset['sector'] == sector['id']), 2)
        sector['percentage'] = round(sector['value'] / portfolio_value * 100, 2)

    for data in portfolio_data:
        sector_value = [sector['value'] for sector in all_sectors if
                        data['sector'] == sector['id'] and 'value' in sector]
        data['sector_percentage'] = round(data['asset_value'] / sector_value[0] * 100, 2)

    result = sorted(all_sectors, key=lambda k: k['value'], reverse=True)
    return result


def prepare_portfolio_data(portfolio_data):
    for data in portfolio_data:
        quantity = data['quantity']
        buyin = data['buyIn']
        price = data['regularMarketPrice']
        priceOpen = data['regularMarketOpen']

        value = calc_asset_value(quantity, price)

        profit_total_absolute, profit_total_relative, profit_today_absolute, profit_today_relative = calc_asset_profit(
            value, quantity, buyin, priceOpen)

        data['asset_value'] = value
        data['profit_total_absolute'] = profit_total_absolute
        data['profit_total_relative'] = profit_total_relative
        data['profit_today_absolute'] = profit_today_absolute
        data['profit_today_relative'] = profit_today_relative

        # only for stocks
        if 'trailingAnnualDividendRate' in data:
            dividended_rate, dividended_yield, my_dividend = calc_asset_dividend(data['trailingAnnualDividendRate'],
                                                                                 data['trailingAnnualDividendYield'],
                                                                                 quantity)
            data['trailingAnnualDividendRate'] = dividended_rate
            data['trailingAnnualDividendYield'] = dividended_yield
            data['dividend'] = my_dividend

    # sector percentage

    return portfolio_data


def update_portfolio_data(conn):
    portfolio_data = select_portfolios_data_for_prepare(conn)
    portfolio_data = prepare_portfolio_data(portfolio_data)

    update_all_portfolio_data(conn, portfolio_data)


def prepare_portfolios(conn, portfolios):
    for portfolio in portfolios:
        portfolio_assets = select_portfolio_data(conn, portfolio['id'])

        portfolio_value = calc_portfolio_value(portfolio_assets)

        profit_total_absolute, profit_total_relative, profit_today_absolute, profit_today_relative = calc_portfolio_profit(
            portfolio_assets)

        my_dividend = calc_portfolio_dividend(portfolio_assets)

        portfolio['portfolio_value'] = portfolio_value
        portfolio['profit_total_absolute'] = profit_total_absolute
        portfolio['profit_total_relative'] = profit_total_relative
        portfolio['profit_today_absolute'] = profit_today_absolute
        portfolio['profit_today_relative'] = profit_today_relative
        portfolio['dividend'] = my_dividend

    # all_portfolios = {'value': calc_portfolio_value(assets), 'profit_total': (calc_portfolio_profit(assets))[0],
    #                 'profit_today': (calc_portfolio_profit(assets))[1], 'dividend': calc_portfolio_dividend(assets)}

    return portfolios  # , all_portfolios


def update_portfolios(conn):
    portfolios = select_all_portfolios_for_preparation(conn)
    portfolios = prepare_portfolios(conn, portfolios)

    update_all_portfolios(conn, portfolios)
