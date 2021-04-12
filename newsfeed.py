import json
from datetime import datetime
import locale

import requests

# ToDo: amount of headlines
import xmltodict as xmltodict

from utils import search_alternative_symbols

"""
https://rss2json.com/docs
"""


def get_news_for_ticker(symbols, key=''):
    def send_request(symbols):
        url = 'http://feeds.finance.yahoo.com/rss/2.0/headline?s='
        if len(symbols) > 0 and symbols[0] is None:
            return None
        if isinstance(symbols, list):
            symbols = ','.join(symbols)

        url = url + symbols
        url = '{}&lang={}'.format(url, 'de-DE,en-US')
        data = requests.get(url).text
        data = json.loads(json.dumps(xmltodict.parse(data)))

        return data['rss']['channel']

    def parse_data(data):
        if 'item' in data and len(data['item']) > 0:
            for event in data['item']:
                # shorten description
                if len(event['description']) > max_description_length:
                    event['description_prev'] = event['description'][:max_description_length] + '...'
                else:
                    event['description_prev'] = event['description']

                pubDate = datetime.strptime(event['pubDate'], '%a, %d %b %Y %H:%M:%S +0000')
                event['pubDate'] = pubDate.strftime("%a, %m %b, %H:%M")
            return data['item']

        return None

    max_description_length = 500

    result = None
    data = send_request(symbols)
    result = parse_data(data)

    if result is None and isinstance(symbols, list) is False:
        alternative_symbols = search_alternative_symbols(symbols)
        if len(alternative_symbols) > 0:
            symbols = [symbol['symbol'] for symbol in alternative_symbols]
            symbols = ','.join(symbols)
            data = send_request(symbols)
            result = parse_data(data)

    return result
