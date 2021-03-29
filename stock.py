import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

import requests


def get_historical_data(symbol):
    # [2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]

    now = datetime.now()
    period2 = str(datetime.timestamp(now)).split('.')[0]
    period1 = str(datetime.timestamp(now - relativedelta(days=300))).split('.')[0]
    period2 = period2.split('.')[0]
    period1 = period1.split('.')[0]
    interval = '60m'

    url = 'https://query1.finance.yahoo.com/v8/finance/chart/?symbol={}&period1={}&period2={}&interval={}&chart'.format(
        symbol, period1, period2, interval)

    result = requests.get(url)

    result = result.json()

    timestamps = result['chart']['result'][0]['timestamp']

    data_high = result['chart']['result'][0]['indicators']['quote'][0]['high']
    data_low = result['chart']['result'][0]['indicators']['quote'][0]['low']

    assert (len(data_low) == len(data_low) == len(timestamps))
    data = {}

    for i in range(len(data_high)):
        if data_high[i] is not None:
            data[str(datetime.fromtimestamp(timestamps[i])).replace(' ', 'T')] = (data_high[i] + data_low[i]) / 2

    timestamps = [timestamp for timestamp in data.keys()]
    data = [key for key in data.values()]

    return json.dumps(data), json.dumps(timestamps)


