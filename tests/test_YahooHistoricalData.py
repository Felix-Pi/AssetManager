from unittest import TestCase
import pandas as pd
import yfinance as yf

from app.domain_logic.YahooHistoricalData import get_historical_data, get_historical_data_for_portfolio


class Test(TestCase):
    def test_get_historical_data(self):
        res = get_historical_data('APC.F', '3mo', '1h')

        print(res)

    def test_get_historical_data_for_multiple_symbols(self):
        res = get_historical_data_for_portfolio(1, '3mo', '1h', return_json=True, domain='user')
        pd.set_option("display.max_rows", None, "display.max_columns", None)

        #print(res)

