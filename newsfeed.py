from datetime import datetime

import requests

# ToDo: amount of headlines
from utils import search_alternative_symbols

"""
https://rss2json.com/docs
"""


def get_news_for_ticker(symbols, key=''):
    def send_request(symbols):
        url = 'https://api.rss2json.com/v1/api.json?rss_url=http://feeds.finance.yahoo.com/rss/2.0/headline?s='
        if len(symbols) > 0 and symbols[0] is None:
            return None
        if isinstance(symbols, list):
            symbols = ','.join(symbols)

        url = url + symbols
        url = '{}&lang={}'.format(url, 'de-DE,en-US')
        return requests.get(url).json()

    def parse_data(data):
        if data['status'] == 'ok' and len(data['items']) > 0:
            for event in data['items']:
                # shorten description
                if len(event['description']) > max_description_length:
                    event['description_prev'] = event['description'][:max_description_length] + '...'
                else:
                    event['description_prev'] = event['description']

                # format pubDate
                pubDate = datetime.strptime(event['pubDate'], '%Y-%m-%d %H:%M:%S')
                event['pubDate'] = pubDate.strftime("%m.%d.%Y, %H:%M")
            return data['items']
        if data['status'] == 'error':
            print('newsfeed.parse_data(): ', data)

        return None

    max_description_length = 500

    result = None
    data = send_request(symbols)
    result = parse_data(data)

    if result is None and isinstance(symbols, list) is False:
        alternative_symbols = search_alternative_symbols(symbols)
        symbols = [symbol['symbol'] for symbol in alternative_symbols]
        symbols = ','.join(symbols)
        data = send_request(symbols)
        result = parse_data(data)

    return result
