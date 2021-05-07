from unittest import TestCase

from app.domain_logic.YahooFinanceApi import YahooFinanceApi


class TestYahooFinanceApi(TestCase):
    def test_get_price(self):
        api = YahooFinanceApi()
        res = api.get_price('AAPL')
        print(res)

        res = api.get_price('AAPL', convert_currency=False)
        print(res)

    def test_get_price(self):
        api = YahooFinanceApi()
        res = api.get_prices(['AAPL', 'APC.F', 'BAYN.DE'])
        print(res)
