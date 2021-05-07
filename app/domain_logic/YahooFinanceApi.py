import json

import requests
from requests_threads import AsyncSession as AsyncSession


class YahooFinanceApi():
    def __init__(self):
        self.base_url = 'https://query1.finance.yahoo.com/'
        self.base_url1 = 'https://query2.finance.yahoo.com/'
        self.quote_summary_url = 'v10/finance/quoteSummary/'
        self.quote_summary_parse_result = ['quoteSummary', 'result']
        self.convert_currency_to = 'EUR'

    def request(self, url, params):
        req = requests.get(self.base_url + url, params=params)
        try:
            return req.json()
        except ValueError:
            return None

    def parse_quote_summary(self, result):
        for param in self.quote_summary_parse_result:
            if param not in result:
                return False

            result = result[param]

        return result[0]['price']

    def get_currency(self, currency_symbol):
        params = {
            'symbol': currency_symbol,
            'modules': 'price'
        }
        data = self.request(self.quote_summary_url, params)
        data = self.parse_quote_summary(data)

        return data['regularMarketPrice']['raw']

    def convert_currency(self, symbol, data, debug=True):
        blacklist = ['currency']
        currency = data['currency']

        if 'currency' not in data or currency == 'EUR':
            return data

        currency_symbol = '{}{}=X'.format(currency, self.convert_currency_to)

        course = self.get_currency(currency_symbol)
        data = {x: round(data[x] * course, 2) for x in data if x not in blacklist}
        data['currency'] = self.convert_currency_to

        return data

    def get_price(self, symbol, convert_currency=True):
        params = {
            'symbol': symbol,
            'modules': 'price'
        }
        data = self.request(self.quote_summary_url, params)
        data = self.parse_quote_summary(data)

        data = {'price': data['regularMarketPrice']['raw'],
                'price_open': data['regularMarketOpen']['raw'],
                'currency': data['currency']}

        if convert_currency:
            return self.convert_currency(symbol, data)

        return data

    def get_prices(self, symbols, convert_currency=True):
        session = AsyncSession(n=10)

        base_url = '{}{}?modules=price&symbol='.format(self.base_url, self.quote_summary_url)
        base_url1 = '{}{}?modules=price&symbol='.format(self.base_url1, self.quote_summary_url)

        async def _main():
            rs = {}
            counter = 0
            for symbol in symbols:
                counter += 1
                if counter % 2 == 0:
                    url = base_url + symbol
                else:
                    url = base_url1 + symbol

                data = await session.get(url)
                data = self.parse_quote_summary(data.json())

                data = {'price': data['regularMarketPrice']['raw'],
                        'price_open': data['regularMarketOpen']['raw'],
                        'currency': data['currency']}

                if convert_currency:
                    data = self.convert_currency(symbol, data)

                rs[symbol] = data

            print(json.dumps(rs))

        session.run(_main)


# main.py
import sys

if __name__ == "__main__":
    api = YahooFinanceApi()
    symbols = sys.argv[1]
    symbols = symbols.split(',')
    api.get_prices(symbols)
