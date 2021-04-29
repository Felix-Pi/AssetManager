from flask import render_template, request, url_for
from flask_breadcrumbs import register_breadcrumb

from app import db, Asset, Portfolio_positions, Portfolio
from app.routes.asset import bp


def view_user_dlc(*args, **kwargs):
    portfolio_id = request.view_args['portfolio_id']
    symbol = request.view_args['symbol']

    return [{'text': symbol, 'url': url_for('asset.asset_index', symbol=symbol, portfolio_id=portfolio_id)}]


@bp.route('/<int:portfolio_id>/<string:symbol>/')
@register_breadcrumb(bp, '.portfolio.asset_index', 'Asset', dynamic_list_constructor=view_user_dlc)
def asset_index(portfolio_id, symbol):
    asset = db.session.query(Asset).filter_by(symbol=symbol).first()
    position = db.session.query(Portfolio_positions).filter(Portfolio_positions.symbol == symbol,
                                                            Portfolio_positions.portfolio == portfolio_id).first()

    general_info = {
        'title': asset.get_property('title'),
        'symbol': asset.get_property('symbol'),
        'Website': asset.get_property('website'),
        'sector': asset.get_property('sector'),
        'industry': asset.get_property('industry'),
        'fullTimeEmployees': asset.get_property('fullTimeEmployees'),
        'description': asset.get_property('longBusinessSummary'),
    }

    financials = {
        'price': {
            'price': asset.get_property('price'),
            'price open': asset.get_property('price_open'),
            'volume': asset.get_property('regularMarketVolume'),
            'day low': asset.get_property('regularMarketDayLow'),
            'day hig': asset.get_property('regularMarketDayHigh'),
            'averageVolume': asset.get_property('averageVolume'),
            'bid': asset.get_property('bid'),
            'ask': asset.get_property('ask'),
        },
        'price_more': {
            'regularMarketPrice': asset.get_property('price'),
            'regularMarketOpen': asset.get_property('price_open'),
            'regularMarketVolume': asset.get_property('regularMarketVolume'),
            'regularMarketDayLow': asset.get_property('regularMarketDayLow'),
            'regularMarketDayHigh': asset.get_property('regularMarketDayHigh'),
            'dayLow': asset.get_property('dayLow'),
            'dayHigh': asset.get_property('dayHigh'),
            'trailingPE': asset.get_property('trailingPE'),
            'forwardPE': asset.get_property('forwardPE'),
            'volume': asset.get_property('volume'),
            'averageVolume': asset.get_property('averageVolume'),
            'averageVolume10days': asset.get_property('averageVolume10days'),
            'bid': asset.get_property('bid'),
            'ask': asset.get_property('ask'),
            'bidSize': asset.get_property('bidSize'),
            'askSize': asset.get_property('askSize'),
            'marketCap': asset.get_property('marketCap'),
            'fiftyTwoWeekLow': asset.get_property('fiftyTwoWeekLow'),
            'fiftyTwoWeekHigh': asset.get_property('fiftyTwoWeekHigh'),
            'fiftyDayAverage': asset.get_property('fiftyDayAverage'),
            'twoHundredDayAverage': asset.get_property('twoHundredDayAverage'),
        },
        'dividend': {
            'dividend_rate': asset.get_property('dividend_rate'),
            'dividendYield': asset.get_property('dividendYield'),
            'exDividendDate': asset.get_property('exDividendDate'),
            'trailingAnnualDividendRate': asset.get_property('trailingAnnualDividendRate'),
            'trailingAnnualDividendYield': asset.get_property('trailingAnnualDividendYield'),
        },
        'company_financials': {
            'totalCash': asset.get_property('totalCash'),
            'totalCashPerShare': asset.get_property('totalCashPerShare'),
            'totalDebt': asset.get_property('totalDebt'),
            'totalRevenue': asset.get_property('totalRevenue'),
            'debtToEquity': asset.get_property('debtToEquity'),
            'revenuePerShare': asset.get_property('revenuePerShare'),
            'freeCashflow': asset.get_property('freeCashflow'),
            'operatingCashflow': asset.get_property('operatingCashflow'),
            'earningsGrowth': asset.get_property('earningsGrowth'),
            'revenueGrowth': asset.get_property('revenueGrowth'),
        },
        'earnings': asset.parse_earnings(),
    }

    events = {
        'Dividend date': asset.get_property('dividend_date'),
        'Ex dividend date': asset.get_property('ex_dividend_date'),
    }

    print(events)
    templateData = {
        'asset': asset,
        'position': position,
        'general_info': general_info,
        'financials': financials,
        'events': events,
        'ownership': financials,
    }

    return render_template('assets/base.html', **templateData, title=('Home'))
