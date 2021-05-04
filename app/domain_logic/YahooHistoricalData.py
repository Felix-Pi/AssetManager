import json

import yfinance as yf
import pandas as pd

# locale.setlocale(locale.LC_TIME, "de_DE")
from app import db, Portfolio, User


def get_historical_data_for_portfolio(id, period, interval, return_json=True, domain='portfolio'):
    pd.set_option("display.max_rows", None, "display.max_columns", None)

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

    print(len(transactions))

    symbols = [s['symbol'] for s in positions]

    ticker_list = ' '.join(symbols)

    tickers = yf.Tickers(ticker_list)

    print(tickers)

    df = tickers.history(period, interval)

    del df['Open']
    del df['Close']
    del df['Volume']
    del df['Dividends']
    del df['Stock Splits']

    cols = ['High', 'Low']

    for symbol in symbols:
        df_symbol = df['High'][symbol].fillna(method='backfill').fillna(method='ffill').items()
        quantity = None
        day = None
        refresh_quantity = True
        for timesamp, value in df_symbol:
            if ('1d' == period or '2d' == period) and timesamp.strftime("%H:%M") == '12:00':
                quantity = None
            else:
                if day != timesamp.strftime("%d"):
                    quantity = None

            if quantity is None:
                quantity = pf.calc_position(symbol=symbol, transactions=transactions, until_data=timesamp)[
                    'quantity']

            day = timesamp.strftime("%d")

            df['High'][symbol][timesamp] *= quantity
            df['Low'][symbol][timesamp] *= quantity

    df['HighAll'] = df['High'].fillna(method='backfill').fillna(method='ffill').loc[:, symbols].sum(axis=1)
    df['LowAll'] = df['Low'].fillna(method='backfill').fillna(method='ffill').loc[:, symbols].sum(axis=1)

    df['Median'] = (df['HighAll'] + df['LowAll']) / 2

    del df['High']
    del df['Low']

    del df['HighAll']
    del df['LowAll']

    df['timestamps'] = df['Median'].keys()
    df = parse_historical_data(df, period)

    # remove multi level column
    df.columns = [col[0] for col in df.columns]

    df.to_csv('data/csv/{}/{}_{}_{}_{}.csv'.format(domain, domain, id, period, interval))

    if return_json:
        return df.to_json()

    return df


def get_historical_data(symbol, period, interval, return_json=True):
    print(symbol, period, interval)
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

    pd.set_option("display.max_rows", None, "display.max_columns", None)

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
