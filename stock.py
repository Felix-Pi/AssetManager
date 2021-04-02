import json
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

import requests


def request_historical_data(symbol, days, interval):
    now = datetime.now()
    period2 = str(datetime.timestamp(now)).split('.')[0]  # prev format: 1617109848.86177
    period1 = str(datetime.timestamp(now - relativedelta(days=int(days)))).split('.')[0]
    period2 = period2.split('.')[0]
    period1 = period1.split('.')[0]

    url = 'https://query1.finance.yahoo.com/v8/finance/chart/?symbol={}&period1={}&period2={}&interval={}&chart'.format(
        symbol, period1, period2, interval)

    result = requests.get(url)

    return result.json()


def get_historical_data(symbols, days, interval):
    # [2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
    datasets = []
    symbols = symbols.split(',')
    for symbol in symbols:
        data = request_historical_data(symbol, days, interval)

        timestamps = data['chart']['result'][0]['timestamp']

        high = data['chart']['result'][0]['indicators']['quote'][0]['high']
        low = data['chart']['result'][0]['indicators']['quote'][0]['low']
        open = data['chart']['result'][0]['indicators']['quote'][0]['open']
        close = data['chart']['result'][0]['indicators']['quote'][0]['close']

        assert (len(low) == len(high) == len(timestamps) == len(open) == len(close))
        data_dict = {'timestamps': [], 'timestamps_raw': [], 'high': [], 'low': [], 'open': [], 'close': [],
                     'median': []}

        for i in range(len(high)):
            if high[i] is not None:
                data_dict['title'] = symbol
                data_dict['timestamps'].append(parse_historical_data(timestamps[i], days, interval))
                data_dict['timestamps_raw'].append(timestamps[i])
                data_dict['high'].append(high[i])
                data_dict['low'].append(low[i])
                data_dict['open'].append(open[i])
                data_dict['close'].append(close[i])
                data_dict['median'].append((high[i] + low[i]) / 2)

        datasets.append(data_dict)

    return json.dumps(datasets)


def parse_historical_data(timestamp, days, period):
    now = datetime.now()

    ts_formatted = str(datetime.fromtimestamp(timestamp))
    ts_formatted = datetime.strptime(ts_formatted, '%Y-%m-%d %H:%M:%S')

    if '2m' == period or '5m' == period or '15m' == period:
        ts_formatted = ts_formatted.strftime("%H:%M")
    if '60m' == period:
        ts_formatted = ts_formatted.strftime("%m.%d %H:%M")
    if '1d' == period:
        ts_formatted = ts_formatted.strftime("%m.%d %H:%M")
    if '5d' == period:
        ts_formatted = ts_formatted.strftime("%m.%d.%Y %H:%M")
    if '1mo' == period:
        ts_formatted = ts_formatted.strftime("%m.%d.%Y %H:%M")

    return ts_formatted


def get_asset_profile(symbol):
    url = 'http://query1.finance.yahoo.com//v10/finance/quoteSummary/?symbol={}&modules=assetProfile'.format(symbol)

    data = requests.get(url).json()['quoteSummary']['result']

    result = {'country': '', 'website': '', 'industry': '', 'sector': '', 'longBusinessSummary': '',
              'fullTimeEmployees': ''}

    if data != None:
        data = data[0]['assetProfile']
        print(data)

        if 'country' in data:
            result['country'] = data['country']
        if 'website' in data:
            result['website'] = data['website']
        if 'industry' in data:
            result['industry'] = data['industry']
        if 'sector' in data:
            result['sector'] = data['sector']
        if 'longBusinessSummary' in data:
            result['longBusinessSummary'] = data['longBusinessSummary']
        if 'fullTimeEmployees' in data:
            result['fullTimeEmployees'] = data['fullTimeEmployees']

    print(result)
    return result


def get_recommendation_trend(symbol):
    url = 'http://query1.finance.yahoo.com//v10/finance/quoteSummary/?symbol={}&modules=recommendationTrend'.format(
        symbol)

    data = requests.get(url).json()['quoteSummary']['result']

    result = []
    if data != None:
        data = data[0]['recommendationTrend']['trend']

        for trend in data:
            tmp = {}
            tmp['period'] = trend['period']
            tmp['strongSell'] = trend['strongSell']
            tmp['sell'] = trend['sell']
            tmp['hold'] = trend['hold']
            tmp['buy'] = trend['buy']
            tmp['strongBuy'] = trend['strongBuy']
            result.append(tmp)
    print(result)
    return json.dumps(result)


def get_calendar_events(symbol):
    url = 'http://query1.finance.yahoo.com//v10/finance/quoteSummary/?symbol={}D&modules=calendarEvents'.format(symbol)
    data = requests.get(url).json()
