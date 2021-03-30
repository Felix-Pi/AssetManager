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
        print(symbols, symbol)
        data = request_historical_data(symbol, days, interval)

        timestamps = data['chart']['result'][0]['timestamp']

        data_high = data['chart']['result'][0]['indicators']['quote'][0]['high']
        data_low = data['chart']['result'][0]['indicators']['quote'][0]['low']

        assert (len(data_low) == len(data_low) == len(timestamps))
        data_dict = {}

        for i in range(len(data_high)):
            if data_high[i] is not None:
                data_dict[timestamps[i]] = (data_high[i] + data_low[i]) / 2

        datasets.append(parse_historical_data(symbol, data_dict, interval))

    return json.dumps(datasets)


def parse_historical_data(symbol, data, interval):
    ts = [elem for elem in data.keys()]

    now = datetime.now()

    dataset = {}
    dataset['labels'] = []
    dataset['data'] = []

    for elem in ts:
        elem = datetime.fromtimestamp(elem)

        timestamp = datetime.timestamp(elem)
        timestamp_formatted = str(datetime.fromtimestamp(timestamp))
        timestamp_formatted = datetime.strptime(timestamp_formatted, '%Y-%m-%d %H:%M:%S')

        #timestamp_formatted = timestamp_formatted.strftime('%Y-%m-%d %H:%M:%S')

        if '2m' == interval or '5m' == interval or '15m' == interval:
            timestamp_formatted = timestamp_formatted.strftime("%H:%M")
        if '60m' == interval:
            timestamp_formatted = timestamp_formatted.strftime("%m.%d %H:%M")
        if '1d' == interval:
            timestamp_formatted = timestamp_formatted.strftime("%m.%d %H:%M")
        if '5d' == interval:
            timestamp_formatted = timestamp_formatted.strftime("%m.%d.%Y %H:%M")
        if '1mo' == interval:
            timestamp_formatted = timestamp_formatted.strftime("%m.%d.%Y %H:%M")

            # data-days="1" data-period="15m"
            # data-days="7" data-period="60m"
            # data-days="30" data-period="1d"
            # data-days="365" data-period="5d"
            # data-days="1800" data-period="1mo"

        dataset['labels'].append(timestamp_formatted)
        dataset['data'].append(data[timestamp])

    dataset['title'] = symbol
    return dataset
