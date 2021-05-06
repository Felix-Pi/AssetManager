from unittest import TestCase
import pandas as pd


class Test(TestCase):
    def test_parse_recommendation_trend(self):
        import yfinance as yf
        msft = yf.Ticker('APC.F')

        pd.set_option("display.max_rows", None, "display.max_columns", None)
        df = msft.recommendations

        print(df.columns)
        res = df.groupby(by=[df.index.month])

        for key, item in res:
            #print(res.get_group(key).groupby('To Grade').nunique())
            print(res.get_group(key), "\n\n")


        for x in df:
            print('x: ', x)

data = {'zip': '95014', 'sector': 'Technology', 'fullTimeEmployees': 100000,
        'longBusinessSummary': 'Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. It also sells various related services. The company offers iPhone, a line of smartphones; Mac, a line of personal computers; iPad, a line of multi-purpose tablets; and wearables, home, and accessories comprising AirPods, Apple TV, Apple Watch, Beats products, HomePod, iPod touch, and other Apple-branded and third-party accessories. It also provides AppleCare support services; cloud services store services; and operates various platforms, including the App Store, that allow customers to discover and download applications and digital content, such as books, music, video, games, and podcasts. In addition, the company offers various services, such as Apple Arcade, a game subscription service; Apple Music, which offers users a curated listening experience with on-demand radio stations; Apple News+, a subscription news and magazine service; Apple TV+, which offers exclusive original content; Apple Card, a co-branded credit card; and Apple Pay, a cashless payment service, as well as licenses its intellectual property. The company serves consumers, and small and mid-sized businesses; and the education, enterprise, and government markets. It sells and delivers third-party applications for its products through the App Store. The company also sells its products through its retail and online stores, and direct sales force; and third-party cellular network carriers, wholesalers, retailers, and resellers. Apple Inc. was founded in 1977 and is headquartered in Cupertino, California.',
        'city': 'Cupertino', 'phone': '408-996-1010', 'state': 'CA', 'country': 'United States', 'companyOfficers': [],
        'website': 'http://www.apple.com', 'maxAge': 1, 'address1': 'One Apple Park Way',
        'industry': 'Consumer Electronics', 'previousClose': 127.85, 'regularMarketOpen': 129.2,
        'twoHundredDayAverage': 126.05434, 'trailingAnnualDividendYield': 0.006413766, 'payoutRatio': 0.1834,
        'volume24Hr': None, 'regularMarketDayHigh': 130.44, 'navPrice': None, 'averageDailyVolume10Day': 102000828,
        'totalAssets': None, 'regularMarketPreviousClose': 127.85, 'fiftyDayAverage': 128.302,
        'trailingAnnualDividendRate': 0.82, 'open': 129.2, 'toCurrency': None, 'averageVolume10days': 102000828,
        'expireDate': None, 'yield': None, 'algorithm': None, 'dividendRate': 0.88, 'exDividendDate': 1620345600,
        'beta': 1.219525, 'circulatingSupply': None, 'startDate': None, 'regularMarketDayLow': 128.86, 'priceHint': 2,
        'currency': 'USD', 'trailingPE': 29.116655, 'regularMarketVolume': 49119392, 'lastMarket': None,
        'maxSupply': None, 'openInterest': None, 'marketCap': 2161711513600, 'volumeAllCurrencies': None,
        'strikePrice': None, 'averageVolume': 102014859, 'priceToSalesTrailing12Months': 6.6431212, 'dayLow': 128.86,
        'ask': 129.54, 'ytdReturn': None, 'askSize': 1300, 'volume': 49119392, 'fiftyTwoWeekHigh': 145.09,
        'forwardPE': 24.39548, 'fromCurrency': None, 'fiveYearAvgDividendYield': 1.37, 'fiftyTwoWeekLow': 74.7175,
        'bid': 129.53, 'tradeable': False, 'dividendYield': 0.0069, 'bidSize': 900, 'dayHigh': 130.44,
        'exchange': 'NMS', 'shortName': 'Apple Inc.', 'longName': 'Apple Inc.',
        'exchangeTimezoneName': 'America/New_York', 'exchangeTimezoneShortName': 'EDT', 'isEsgPopulated': False,
        'gmtOffSetMilliseconds': '-14400000', 'quoteType': 'EQUITY', 'symbol': 'AAPL', 'messageBoardId': 'finmb_24937',
        'market': 'us_market', 'annualHoldingsTurnover': None, 'enterpriseToRevenue': 6.716, 'beta3Year': None,
        'profitMargins': 0.23451, 'enterpriseToEbitda': 21.893, '52WeekChange': 0.7010944,
        'morningStarRiskRating': None, 'forwardEps': 5.31, 'revenueQuarterlyGrowth': None,
        'sharesOutstanding': 16687599616, 'fundInceptionDate': None, 'annualReportExpenseRatio': None,
        'bookValue': 4.146, 'sharesShort': 127937929, 'sharesPercentSharesOut': 0.0077, 'fundFamily': None,
        'lastFiscalYearEnd': 1601078400, 'heldPercentInstitutions': 0.60099, 'netIncomeToCommon': 76311003136,
        'trailingEps': 4.449, 'lastDividendValue': 0.205, 'SandP52WeekChange': 0.46209478, 'priceToBook': 31.244572,
        'heldPercentInsiders': 0.00075999997, 'nextFiscalYearEnd': 1664150400, 'mostRecentQuarter': 1616803200,
        'shortRatio': 1.29, 'sharesShortPreviousMonthDate': 1615766400, 'floatShares': 16670275864,
        'enterpriseValue': 2185324658688, 'threeYearAverageReturn': None, 'lastSplitDate': 1598832000,
        'lastSplitFactor': '4:1', 'legalType': None, 'lastDividendDate': 1612483200, 'morningStarOverallRating': None,
        'earningsQuarterlyGrowth': 1.101, 'dateShortInterest': 1618444800, 'pegRatio': 1.46, 'lastCapGain': None,
        'shortPercentOfFloat': 0.0077, 'sharesShortPriorMonth': 107011007, 'impliedSharesOutstanding': None,
        'category': None, 'fiveYearAverageReturn': None, 'regularMarketPrice': 129.54,
        'logo_url': 'https://logo.clearbit.com/apple.com'}
