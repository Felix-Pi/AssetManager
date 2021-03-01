import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

import requests


def get_historical_data():
    # [2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]

    now = datetime.now()
    period2 = str(datetime.timestamp(now)).split('.')[0]
    period1 = str(datetime.timestamp(now - relativedelta(days=3))).split('.')[0]

    period2 = period2.split('.')[0]
    period1 = period1.split('.')[0]
    interval = '30m'

    url = 'https://query1.finance.yahoo.com/v8/finance/chart/?symbol=APC.F&period1={}&period2={}&interval={}&chart'.format(
        period1, period2, interval)

    result = requests.get(url)

    result = result.json()

    timestamps = result['chart']['result'][0]['timestamp']

    data = result['chart']['result'][0]['indicators']['quote'][0]['high']

    print(len(timestamps), len(data))

    for i in range(len(data)):
        pos = len(data) - 1 - i

        print(pos, timestamps[i], data[i])
        if data[pos] is None:
            timestamps.remove(pos)
            data.remove(pos)

    # for i in range(len(data)):
    #     timestamps[i] = str(datetime.fromtimestamp(timestamps[i])).replace(' ', '_')
    #     print(timestamps[i], '-', data[i])

    print(url)
    return json.dumps(data), json.dumps(timestamps)


if __name__ == '__main__':
    data = get_historical_data()

    print()
