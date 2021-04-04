import json
import re
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

import requests

from utils import yahoo_search_request, search_alternative_symbols


def get_top_holdings(symbol):
    def send_request(symbol):
        url = 'http://query1.finance.yahoo.com//v10/finance/quoteSummary/?symbol={}&modules=topHoldings'.format(
            symbol)

        data = requests.get(url).json()['quoteSummary']['result']
        return data

    def parse_data(data):
        result = None

        result = {'holdings': [], 'sectorWeightings': []}

        if data != None:
            data = data[0]['topHoldings']

            if 'holdings' in data:
                result['holdings'] = data['holdings']
            if 'sectorWeightings' in data:
                result['sectorWeightings'] = data['sectorWeightings']

            return data
        return result

    def check_alternative_symbols(symbols):
        for symbol in symbols:
            data = send_request(symbol['symbol'])
            result = parse_data(data)
            if result is not None:
                # print('Alternative result found: \'{}\''.format(symbol['symbol']))
                # print('Data: \'{}\''.format(data))
                return result

    data = send_request(symbol)
    result = parse_data(data)

    # if result is None:
    #     alternative_symbols = search_alternative_symbols(symbol)
    #     result = check_alternative_symbols(alternative_symbols)

    print('etf.py: json.dumps(result)=', json.dumps(result))


    print(result)
    return result
