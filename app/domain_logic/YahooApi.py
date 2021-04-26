import copy

import sqlalchemy
from pip._vendor import requests

# https://query2.finance.yahoo.com/v6/finance/quote/validate?symbols=MSFT validate symbol
from app import app

# https://stackoverflow.com/questions/44030983/yahoo-finance-url-not-working
# https://observablehq.com/@stroked/yahoofinance
# https://github.com/pilwon/node-yahoo-finance/issues/43

modules = ['assetProfile', 'summaryProfile', 'recommendationTrend', 'indexTrend', 'fundOwnership', 'summaryProfile',
           'summaryDetail', 'calendarEvents', 'financialData', 'secFilings', 'price', 'upgradeDowngradeHistory',
           # 'assetProfile', 'esgScores', 'defaultKeyStatistics', 'incomeStatementHistory', 'incomeStatementHistoryQuarterly',
           # 'balanceSheetHistory', 'balanceSheetHistoryQuarterly', 'cashflowStatementHistory',
           # 'cashflowStatementHistoryQuarterly', 'institutionOwnership', 'majorDirectHolders', 'majorHoldersBreakdown',
           # 'insiderTransactions', 'insiderHolders', 'netSharePurchaseActivity', 'earnings', 'earningsHistory',
           # 'earningsTrend', 'industryTrend', 'sectorTrend'
           ]


# price.quoteType = asset type EQUITY, CRYPTOCURRENCY, ETF,

class YahooApi:
    def __init__(self):
        self.url = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/'
        # self.usd_eur = self.build_data('USDEUR=X', usd_eur)['course']
        self.usd_eur = 1

    def request(self, url, params):
        response = requests.get(url, params=params).json()

        return response

    def get_stock_data(self, symbol, modules):
        params = {
            'symbol': symbol,
            'modules': ','.join(modules),
        }

        return self.request(self.url, params)

    def get_symbol_currency(self, symbol):
        params = {
            'symbol': symbol,
            'modules': 'summaryDetail',
        }

        data = self.request(self.url, params)
        data = data['quoteSummary']['result'][0]
        return data['summaryDetail']['currency']

    def parse(self, template, data, symbol):
        """
        parses request data to asset_template format
        :param template:
        :param data:
        :return:
        """
        data = data['quoteSummary']['result'][0]

        currency = self.get_symbol_currency(symbol)

        def get(value):
            """
            returns value from request_data
            value format: module.key.key = value
            :param elem: path do value, seperated by dots. ex: price.regularMarketChangePercent.raw
            :return: value from request_data
            """

            if '.' not in value:
                return None

            target = value.split('.')
            module = target[0]

            if module in data:
                elem = data[module]
                for key in target[1:]:
                    if isinstance(elem, dict) and key in elem:
                        elem = elem[key]
                    elif isinstance(elem, list):
                        key = int(key)
                        elem = elem[int(key)]
                    else:
                        return sqlalchemy.sql.null()

                return elem
            return sqlalchemy.sql.null()

        def execute_options(key):
            def parse_result(value):
                if value is None:
                    # return ''
                    return sqlalchemy.sql.null()
                return value

            def convert_currency(value, currency_to):  # todo
                return value

            if '|' in key:
                key, options = key.split('|')
                value = get(key)

                if options == 'convert_currency':
                    value = convert_currency(value, 'EUR')
                if options == 'toString':
                    value = str(value)
            else:
                value = get(key)
            return parse_result(value)

        def insert_data(template):
            """
            template form: dict { dict_title {setting: value} }
            :param template:
            :return:
            """
            for k, v in template.items():
                if isinstance(v, dict):
                    insert_data(v)
                else:
                    template[k] = execute_options(v)
                    # template[k] = get(v)
            return template

        return insert_data(template)

    def build_data(self, symbol, template):
        app.logger.info('Requestung data for \'{}\' Modules: {}'.format(symbol, template['modules']))
        template = copy.deepcopy(template)
        data = self.get_stock_data(symbol, template['modules'])
        data = self.parse(template, data, symbol)
        return data
