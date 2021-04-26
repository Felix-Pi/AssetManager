stock_api_template = {
    'modules': ['summaryProfile', 'recommendationTrend', 'indexTrend', 'fundOwnership',
                'summaryProfile', 'summaryDetail', 'calendarEvents', 'financialData', 'secFilings', 'price'],

    # general
    'name': '',
    'symbol': '',
    'country': 'summaryProfile.country',
    'website': 'summaryProfile.website',
    'industry': 'summaryProfile.industry',
    'sector': 'summaryProfile.sector',
    'longBusinessSummary': 'summaryProfile.longBusinessSummary',
    'fullTimeEmployees': 'summaryProfile.fullTimeEmployees',

    # # price
    'price': 'price.regularMarketPrice.raw|convert_currency',
    'price_open': 'price.regularMarketOpen.raw|convert_currency',
    'regularMarketVolume': 'price.regularMarketVolume.raw|convert_currency',
    'regularMarketDayLow': 'price.regularMarketDayLow.raw|convert_currency',
    'regularMarketDayHigh': 'price.regularMarketDayHigh.raw|convert_currency',
    'dayLow': 'summaryDetail.dayLow.raw|convert_currency',
    'dayHigh': 'summaryDetail.dayHigh.raw|convert_currency',
    'trailingPE': 'summaryDetail.trailingPE.raw',
    'forwardPE': 'summaryDetail.forwardPE.raw',
    'volume': 'summaryDetail.volume.raw|convert_currency',
    'averageVolume': 'summaryDetail.averageVolume.raw|convert_currency',
    'averageVolume10days': 'summaryDetail.averageVolume10days.raw|convert_currency',
    'bid': 'summaryDetail.bid.raw|convert_currency',
    'ask': 'summaryDetail.ask.raw|convert_currency',
    'bidSize': 'summaryDetail.bidSize.raw',
    'askSize': 'summaryDetail.askSize.raw',
    'marketCap': 'summaryDetail.marketCap.raw|convert_currency',
    'fiftyTwoWeekLow': 'summaryDetail.fiftyTwoWeekLow.raw|convert_currency',
    'fiftyTwoWeekHigh': 'summaryDetail.fiftyTwoWeekHigh.raw|convert_currency',
    'fiftyDayAverage': 'summaryDetail.fiftyDayAverage.raw|convert_currency',
    'twoHundredDayAverage': 'summaryDetail.twoHundredDayAverage.raw|convert_currency',
    'exchange': 'price.exchange',
    'exchange_name': 'price.exchangeName',
    'quote_type': 'price.quoteType',
    'underlying_symbol': 'price.underlyingSymbol',

    # # dividend
    'dividend_rate': 'summaryDetail.dividendRate.raw|convert_currency',
    'dividendYield': 'summaryDetail.dividendYield.raw|convert_currency',
    'exDividendDate': 'summaryDetail.exDividendDate.raw|format_data',
    'trailingAnnualDividendRate': 'summaryDetail.trailingAnnualDividendRate.raw',  # todo currency
    'trailingAnnualDividendYield': 'summaryDetail.fiveYearAvgDividendYield.raw',  # todo currency
    'fiveYearAvgDividendYield': 'summaryDetail.fiveYearAvgDividendYield.raw',  # todo currency

    # # financial data
    'currency': 'summaryDetail.currency.raw',
    'totalCash': 'financialData.totalCash.raw',
    'totalCashPerShare': 'financialData.totalCashPerShare.raw',
    'totalDebt': 'financialData.totalDebt.raw',
    'totalRevenue': 'financialData.totalRevenue.raw',
    'debtToEquity': 'financialData.debtToEquity.raw',
    'revenuePerShare': 'financialData.revenuePerShare.raw',
    'freeCashflow': 'financialData.freeCashflow.raw',
    'operatingCashflow': 'financialData.operatingCashflow.raw',
    'earningsGrowth': 'financialData.earningsGrowth.raw',
    'revenueGrowth': 'financialData.revenueGrowth.raw',

    # # recommendation
    'recommendation_trend': 'recommendationTrend.trend|toString',
    'targetHighPrice': 'financialData.targetHighPrice.raw|convert_currency',
    'targetLowPrice': 'financialData.targetLowPrice.raw|convert_currency',
    'targetMeanPrice': 'financialData.targetMeanPrice.raw|convert_currency',
    'targetMedianPrice': 'financialData.targetMedianPrice.raw|convert_currency',
    'recommendationMean': 'financialData.recommendationMean.raw|convert_currency',
    'recommendationKey': 'financialData.recommendationKey.raw',
    'numberOfAnalystOpinions': 'financialData.numberOfAnalystOpinions.raw',

    # # other
    'ex_dividend_date': 'calendarEvents.exDividendDate.fmt',
    'dividend_date': 'calendarEvents.dividendDate.fmt',

    'earnings': 'calendarEvents.earnings|toString',
    'filings': 'secFilings.filings|toString',
    'ownershipList': 'fundOwnership.ownershipList|toString',
}

etf_api_template = {
    'modules': ['price'],
    'symbol': '',
    # # price
    'price': 'price.regularMarketPrice.raw|convert_currency',
    'price_open': 'price.regularMarketOpen.raw|convert_currency',
    'regularMarketVolume': 'price.regularMarketVolume.raw|convert_currency',
    'regularMarketDayLow': 'price.regularMarketDayLow.raw|convert_currency',
    'regularMarketDayHigh': 'price.regularMarketDayHigh.raw|convert_currency',
    'dividend_rate': 'summaryDetail.dividendRate.raw|convert_currency',
}

crypto_api_template = {
    'modules': ['price'],
    'symbol': '',
    # # price
    'price': 'price.regularMarketPrice.raw|convert_currency',
    'price_open': 'price.regularMarketOpen.raw|convert_currency',
    'regularMarketVolume': 'price.regularMarketVolume.raw|convert_currency',
    'regularMarketDayLow': 'price.regularMarketDayLow.raw|convert_currency',
    'regularMarketDayHigh': 'price.regularMarketDayHigh.raw|convert_currency',
}

usd_eur = {
    'modules': ['price'],
    'course': 'price.regularMarketPrice.raw'
}

price_template = {
    'modules': ['price'],
    'price': 'price.regularMarketPrice.raw|convert_currency',
    'price_open': 'price.regularMarketOpen.raw|convert_currency',
}
