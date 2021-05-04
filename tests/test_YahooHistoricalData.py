from unittest import TestCase

from app.domain_logic.YahooHistoricalData import get_historical_data


class Test(TestCase):
    def test_get_historical_data(self):
        res = get_historical_data('APC.F', '3mo', '1h')
