import json

import yfinance as yf
import pandas as pd

# locale.setlocale(locale.LC_TIME, "de_DE")
from app import db, Portfolio, User, app
from app.domain_logic.utils import delete_key_from_dict


def get_historical_data_for_portfolio(id, period, interval, domain='portfolio'):
    if domain == 'index':
        user = db.session.query(User).filter_by(id=id).first()

        transactions = []
        positions = []

        for portfolio in user.portfolios.all():
            pf = portfolio
            for tr in portfolio.transactions.all():
                transactions.append(tr)

            for pos in portfolio.positions:
                positions.append(pos)

    else:
        pf = db.session.query(Portfolio).filter_by(id=id).first()
        transactions = pf.transactions.all()
        positions = pf.positions

    symbols = [s['symbol'] for s in positions]

    tickers = yf.Tickers(' '.join(symbols))

    df = tickers.history(period, interval)

    delete_key_from_dict(df, ['Open', 'Close', 'Volume', 'Dividends', 'Stock Splits'])

    for symbol in symbols:
        df_symbol = df['High'][symbol].fillna(method='backfill').fillna(method='ffill').items()
        quantity = None
        day = None

        for timesamp, value in df_symbol:
            if ('1d' == period or '2d' == period) and timesamp.strftime("%H:%M") == '12:00':
                quantity = None
            else:
                if day != timesamp.strftime("%d"):
                    quantity = None

            if quantity is None:
                transactions_for_symbol = [t for t in transactions if t.symbol == symbol]
                quantity = pf.calc_position(symbol=symbol, transactions=transactions_for_symbol, until_data=timesamp)[
                    'quantity']

            day = timesamp.strftime("%d")

            df['High'][symbol][timesamp] *= quantity
            df['Low'][symbol][timesamp] *= quantity

    df['HighAll'] = df['High'].fillna(method='backfill').fillna(method='ffill').loc[:, symbols].sum(axis=1)
    df['LowAll'] = df['Low'].fillna(method='backfill').fillna(method='ffill').loc[:, symbols].sum(axis=1)

    df['Median'] = (df['HighAll'] + df['LowAll']) / 2

    delete_key_from_dict(df, ['High', 'Low', 'HighAll', 'LowAll'])

    df['timestamps'] = df['Median'].keys()

    df = parse_historical_data(df, period)

    # remove multi level column
    df.columns = [col[0] for col in df.columns]

    df.to_csv('data/csv/{}/{}_{}_{}_{}.csv'.format(domain, domain, id, period, interval))

    return df


def get_historical_data(symbol, period, interval, return_json=True):
    print(symbol, period, interval)
    app.logger.info('Getting historical data for: \'{}\''.format(symbol))
    symbol = yf.Ticker(symbol)
    hist = symbol.history(period=period, interval=interval)

    hist['Open'].fillna(method='backfill').fillna(method='ffill')
    hist['High'].fillna(method='backfill').fillna(method='ffill')
    hist['Low'].fillna(method='backfill').fillna(method='ffill')
    hist['Close'].fillna(method='backfill').fillna(method='ffill')

    hist['Median'] = ((hist['High'] + hist['Low']) / 2)
    hist['Median'].fillna(method='backfill').fillna(method='ffill')
    hist['timestamps'] = hist['High'].keys()

    hist = parse_historical_data(hist, period)

    if return_json:
        return hist.to_json()

    return hist


def parse_historical_data(df, period):
    if '1d' == period:
        df['timestamps'] = df['timestamps'].dt.strftime("%H:%M")
    if '2d' == period:
        df['timestamps'] = df['timestamps'].dt.strftime("%a, %H:%M")
    if '5d' == period:
        df['timestamps'] = df['timestamps'].dt.strftime("%a, %d %b %H:%M")
    if '1mo' == period:
        df['timestamps'] = df['timestamps'].dt.strftime("%d %b, %H:%M")
    if '3mo' == period:
        df['timestamps'] = df['timestamps'].dt.strftime("%d %b")
    if '1y' == period:
        df['timestamps'] = df['timestamps'].dt.strftime("%d %b %Y")
    if '5y' == period or 'max' == period:
        df['timestamps'] = df['timestamps'].dt.strftime("%b %Y")

    return df
