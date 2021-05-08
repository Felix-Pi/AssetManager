import re
from datetime import datetime

from dateutil.relativedelta import relativedelta


def parse_recommendation_trend(data):
    def parse_label(label):
        # format: 0m, -1m, -2m, -3m
        interval = int(re.findall('[0-3]', label)[0])

        if interval > 0:
            d = datetime.timestamp(datetime.now() - relativedelta(months=interval))
        else:
            d = datetime.timestamp(datetime.now())

        date_time = datetime.fromtimestamp(d)
        return date_time.strftime("%b")

    result = None

    result = {'data': [], 'labels': []}

    for trend in data:
        tmp = {}

        tmp['strongSell'] = trend['strongSell']
        tmp['sell'] = trend['sell']
        tmp['hold'] = trend['hold']
        tmp['buy'] = trend['buy']
        tmp['strongBuy'] = trend['strongBuy']

        if not all(x == 0 for x in tmp.values()):  # check if all values in tmp are zero
            result['data'].append(tmp)
            result['labels'].append(parse_label(trend['period']))

    return result
