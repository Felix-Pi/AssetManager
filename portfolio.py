from mysql import *
from assets import *


def calc_asset_value(quantity, price):
    return round(quantity * price, 2)


def calc_asset_profit(value, quantity, buyin, price_open):
    profit_total_absolute = round(value - (quantity * buyin), 2)

    profit_today_absolute = round(value - (quantity * price_open), 2)

    return profit_total_absolute, profit_today_absolute


def calc_portfolio_value(portfolio_assets):
    return round(sum(asset['asset_value'] for asset in portfolio_assets), 2)

def calc_all_portfolios_value(portfolio_assets):
    return round(sum(asset['portfolio_value'] for asset in portfolio_assets), 2)


def calc_portfolio_profit(portfolio_assets):
    profit_total_absolute = round(sum(asset['profit_total_absolute'] for asset in portfolio_assets), 2)
    profit_today_absolute = round(sum(asset['profit_today_absolute'] for asset in portfolio_assets), 2)

    return profit_total_absolute, profit_today_absolute


def calc_portfolio_dividend(portfolio_assets):
    dividend = round(sum(asset['dividend'] for asset in portfolio_assets), 2)

    return round(dividend, 2)


def prepare_portfolio_data(portfolio_data):
    for data in portfolio_data:
        quantity = data['quantity']
        buyin = data['buyIn']
        price = data['regularMarketPrice']
        priceOpen = data['regularMarketOpen']

        value = calc_asset_value(quantity, price)

        profit_total, profit_today = calc_asset_profit(value, quantity, buyin, priceOpen)

        data['asset_value'] = value
        data['profit_total_absolute'] = profit_total
        data['profit_total_relative'] = profit_total
        data['profit_today_absolute'] = profit_today
        data['profit_today_relative'] = profit_today

        # only for stocks
        if 'trailingAnnualDividendRate' in data:
            dividended_rate, dividended_yield, my_dividend = calc_asset_dividend(data['trailingAnnualDividendRate'],
                                                                                 data['trailingAnnualDividendYield'],
                                                                                 quantity)
            data['trailingAnnualDividendRate'] = dividended_rate
            data['trailingAnnualDividendYield'] = dividended_yield
            data['dividend'] = my_dividend

    return portfolio_data


def update_portfolio_data(conn):
    portfolio_data = select_portfolios_data_for_prepare(conn)
    portfolio_data = prepare_portfolio_data(portfolio_data)

    update_all_portfolio_data(conn, portfolio_data)


def prepare_portfolios(conn, portfolios):
    for portfolio in portfolios:
        portfolio_assets = select_portfolio_data(conn, portfolio['id'])

        portfolio_value = calc_portfolio_value(portfolio_assets)

        portfolio_profit_total, portfolio_profit_today = calc_portfolio_profit(portfolio_assets)

        my_dividend = calc_portfolio_dividend(portfolio_assets)

        portfolio['portfolio_value'] = portfolio_value
        portfolio['profit_total_absolute'] = portfolio_profit_total
        portfolio['profit_total_relative'] = portfolio_profit_total
        portfolio['profit_today_absolute'] = portfolio_profit_today
        portfolio['profit_today_relative'] = portfolio_profit_today
        portfolio['dividend'] = my_dividend

    # all_portfolios = {'value': calc_portfolio_value(static), 'profit_total': (calc_portfolio_profit(static))[0],
    #                 'profit_today': (calc_portfolio_profit(static))[1], 'dividend': calc_portfolio_dividend(static)}

    return portfolios  # , all_portfolios


def update_portfolios(conn):
    portfolios = select_all_portfolios(conn)
    portfolios = prepare_portfolios(conn, portfolios)

    update_all_portfolios(conn, portfolios)
