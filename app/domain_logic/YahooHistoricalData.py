import json
from datetime import datetime

import requests
from dateutil.relativedelta import relativedelta


def request_historical_data(symbol, days, interval):
    now = datetime.now()
    now = str(now).split('.')[0]
    now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')

    period2 = str(datetime.timestamp(now))  # prev format: 1617109848.86177
    period1 = str(datetime.timestamp(now - relativedelta(days=int(days))))
    period2 = str(period2).split('.')[0]
    period1 = str(period1).split('.')[0]

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
        data = data['chart']['result'][0]
        if 'timestamp' not in data:
            return json.dumps([])

        timestamps = data['timestamp']

        high = data['indicators']['quote'][0]['high']
        low = data['indicators']['quote'][0]['low']
        open = data['indicators']['quote'][0]['open']
        close = data['indicators']['quote'][0]['close']

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
    # pubDate.strftime("%a, %m %b, %H:%M")
    if '2m' == period or '5m' == period or '15m' == period:
        ts_formatted = ts_formatted.strftime("%a, %H:%M")
    if '60m' == period:
        ts_formatted = ts_formatted.strftime("%a, %d %b %H:%M")
    if '1d' == period:
        ts_formatted = ts_formatted.strftime("%d %b")
    if '5d' == period:
        ts_formatted = ts_formatted.strftime("%d %b %Y")
    if '1mo' == period:
        ts_formatted = ts_formatted.strftime("%b %Y")

    return ts_formatted