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

    def parse_data_(data):
        result = None

        result = {'holdings': [], 'sectorWeightings': []}

        if data != None:
            data = data[0]['topHoldings']

            if 'holdings' in data:
                result['holdings'] = data['holdings']
            if 'sectorWeightings' in data:
                result['sectorWeightings'] = data['sectorWeightings']

            return result
        return result

    def parse_data(data):
        result = None

        result = {'holdings': [], 'sectorWeightings': []}

        if data != None:
            data = data[0]['topHoldings']

            if 'holdings' in data:
                result['holdings'] = {
                    'raw': data['holdings'],
                    'data': [round(holding['holdingPercent']['raw'] * 100, 2) for holding in data['holdings']],
                    'labels': [holding['holdingName'] for holding in data['holdings']],
                    'symbols': [holding['symbol'] for holding in data['holdings']]
                }

            if 'sectorWeightings' in data:
                for sector in data['sectorWeightings']:
                    sector_title = list(sector.keys())[0]

                    result['sectorWeightings'].append({
                        'sector': sector_title,
                        'sectorWeight': sector[sector_title]
                    })

                result['sectorWeightings'] = sorted(result['sectorWeightings'],
                                                    key=lambda k: k['sectorWeight']['raw'], reverse=True)

                result['sectorWeightings'] = {
                    'raw': result['sectorWeightings'],
                    'data': [round(sector['sectorWeight']['raw'] * 100, 2) for sector in result['sectorWeightings'] if
                             sector['sectorWeight']['raw'] > 0.0],
                    'labels': [sector['sector'].replace('_', ' ').title() for sector in result['sectorWeightings'] if
                               sector['sectorWeight']['raw'] > 0.0]
                }

                # result['sectorWeightings'] = data['sectorWeightings']

            return result
        return result

    data = send_request(symbol)
    result = parse_data(data)

    return result
