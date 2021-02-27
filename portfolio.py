from mysql import *


def get_portfolio_assets(portfolio_id, assets):
    return [asset for asset in assets if asset['portfolio'] == portfolio_id]


def calc_portfolio_value(portfolio_assets):
    return round(sum(asset['value'] for asset in portfolio_assets), 2)


def calc_portfolio_profit(portfolio_assets):
    profit_total_absolute = round(sum(asset['profit_total'] for asset in portfolio_assets), 2)
    profit_today_absolute = round(sum(asset['profit_today'] for asset in portfolio_assets), 2)

    return profit_total_absolute, profit_today_absolute


def calc_portfolio_dividend(portfolio_assets):
    annual_dividends = 0

    for asset in portfolio_assets:
        if 'dividend' in asset:
            annual_dividends += asset['myDividend']

    return round(annual_dividends, 2)


def prepare_portfolios(portfolios, assets):
    for portfolio in portfolios:
        portfolio_assets = get_portfolio_assets(portfolio['id'], assets)

        portfolio_value = calc_portfolio_value(portfolio_assets)

        portfolio_profit_total, portfolio_profit_today = calc_portfolio_profit(portfolio_assets)

        if 'dividend' in portfolio_assets:  # todo check every element
            my_dividend = calc_portfolio_dividend(portfolio_assets)
            portfolio['dividend'] = my_dividend

        portfolio['value'] = portfolio_value
        portfolio['profit_total'] = portfolio_profit_total
        portfolio['profit_today'] = portfolio_profit_today

    all_portfolios = {'value': calc_portfolio_value(assets), 'profit_total': (calc_portfolio_profit(assets))[0],
                      'profit_today': (calc_portfolio_profit(assets))[1], 'dividend': calc_portfolio_dividend(assets)}

    return portfolios, all_portfolios
