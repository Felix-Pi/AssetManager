from flask import render_template

from app import db, Asset
from app.routes.asset import bp


@bp.route('/<string:symbol>/')
def asset_index(symbol):
    asset = db.session.query(Asset).filter_by(symbol=symbol).first()

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
            'regularMarketPrice': asset.get_property('regularMarketPrice'),
            'regularMarketOpen': asset.get_property('regularMarketOpen'),
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
        'general_info': general_info,
        'financials': financials,
        'events': events,
        'ownership': financials,
    }

    return render_template('assets/base.html', **templateData, title=('Home'))
