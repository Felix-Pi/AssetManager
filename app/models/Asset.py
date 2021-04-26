import json
import re
from datetime import datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy import orm

from app import db
from app.domain_logic.YahooApi import YahooApi
from app.domain_logic.asset_templates import stock_api_template, etf_api_template, crypto_api_template, price_template


class Asset(db.Model):
    symbol = db.Column(db.String(64), primary_key=True, unique=True)
    type = db.Column(db.Integer, db.ForeignKey('asset_types.id'))
    type_str = db.relationship("Asset_types")
    price = db.Column(db.Integer)
    price_open = db.Column(db.Integer)
    asset_data_id = db.Column(db.Integer)

    @orm.reconstructor
    def init_on_load(self):
        self.data = self.get_data()

        if self.data is not None:
            self.data = self.data.to_dict()

            for d in self.data:
                setattr(self, d, self.data[d])

    @staticmethod
    def get_symbol(symbol):
        return db.session.query(Asset).filter_by(symbol=symbol).first()

    def get_data(self):
        data = {}
        if self.type == 1:
            data = db.session.query(Stock_data).filter_by(symbol=self.symbol).first()
        if self.type == 2:
            data = db.session.query(Etf_data).filter_by(symbol=self.symbol).first()
        if self.type == 3:
            data = db.session.query(Crypto_data).filter_by(symbol=self.symbol).first()

        return data

    def parse_recommendation_trend(self):
        def parse_label(label):
            # format: 0m, -1m, -2m, -3m
            interval = int(re.findall('[0-3]', label)[0])

            if interval > 0:
                d = datetime.timestamp(datetime.now() - relativedelta(months=interval))
            else:
                d = datetime.timestamp(datetime.now())

            date_time = datetime.fromtimestamp(d)
            return date_time.strftime("%b")

        result = None

        data = self.data['recommendation_trend']

        if data != 'NULL':
            data = json.loads(data.replace('\'', '"'))

            result = {'data': [], 'labels': []}

            for trend in data:
                tmp = {}

                tmp['strongSell'] = trend['strongSell']
                tmp['sell'] = trend['sell']
                tmp['hold'] = trend['hold']
                tmp['buy'] = trend['buy']
                tmp['strongBuy'] = trend['strongBuy']

                if not all(x == 0 for x in tmp.values()):  # check if all values in tmp are zero
                    result['data'].append(tmp)
                    result['labels'].append(parse_label(trend['period']))

        return result

    def to_dict(self):
        data = {
            'symbol': self.symbol,
            'type': self.type,
            'price': self.price,
            'price_open': self.price_open,
            'asset_data_id': self.asset_data_id,
            'data': self.data,
            # 'data': self.data if hasattr(self, 'data') else self.get_data(),
        }

        for d in self.data:
            data[d] = self.data[d]

        return data

    def __repr__(self):
        return '<Asset {}>'.format(self.to_dict())

    @staticmethod
    def get_asset_by_id(id):
        return db.session.query(Asset).filter_by(id=id).first()

    @staticmethod
    def get_asset_by_symbol(symbol):
        return db.session.query(Asset).filter_by(symbol=symbol).first()

    @staticmethod
    def update_all_assets_full():
        for asset in db.session.query(Asset).all():
            Asset.update_asset_full(asset)

        # update_all_portfolio_positions()

    @staticmethod
    def update_asset_full(asset):
        if asset.type == 1:
            template = stock_api_template
        if asset.type == 2:
            template = etf_api_template
        if asset.type == 3:
            template = crypto_api_template

        dataset = YahooApi().build_data(asset.symbol, template)
        dataset.pop('symbol')
        dataset.pop('modules')

        Asset.update_asset_data(asset.symbol, dataset)

    @staticmethod
    def update_asset_data(symbol, dataset):
        asset = db.session.query(Asset).filter_by(symbol=symbol).first()

        asset.price = dataset['price']
        asset.price_open = dataset['price_open']
        db.session.commit()

        if asset.type == 1:
            asset_data = db.session.query(Stock_data).filter_by(symbol=asset.symbol).first()

            asset_data_is_none = asset_data is None
            if asset_data_is_none:
                asset_data = Stock_data(**dataset, symbol=symbol)
        if asset.type == 2:
            asset_data = db.session.query(Etf_data).filter_by(symbol=asset.symbol).first()

            asset_data_is_none = asset_data is None
            if asset_data_is_none:
                asset_data = Etf_data(**dataset, symbol=symbol)
        if asset.type == 3:
            asset_data = db.session.query(Crypto_data).filter_by(symbol=asset.symbol).first()

            asset_data_is_none = asset_data is None
            if asset_data_is_none:
                asset_data = Crypto_data(**dataset, symbol=symbol)

        if asset_data_is_none:
            db.session.add(asset_data)
            db.session.commit()
        else:
            for key in dataset:
                setattr(asset_data, key, dataset[key])

        if asset.asset_data_id is None:
            setattr(asset, 'asset_data_id', asset_data.id)
            db.session.commit()

        db.session.commit()

        return asset

    @staticmethod
    def update_all_assets_price():
        for asset in db.session.query(Asset).all():
            dataset = YahooApi().build_data(asset.symbol, price_template)
            dataset.pop('modules')

            Asset.update_asset_data(asset.symbol, dataset)

        # update_all_portfolio_positions()

    @staticmethod
    def add_symbol(symbol, type):
        fetch_existing = db.session.query(Asset).filter_by(symbol=symbol).first()

        if fetch_existing is not None:
            return fetch_existing

        asset = Asset(symbol=symbol, type=type)

        db.session.add(asset)
        db.session.commit()

        Asset.update_asset_full(asset)

        return asset


class Stock_data(db.Model):
    # general
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.Integer, db.ForeignKey('asset.symbol'), unique=True)
    name = db.Column(db.String())

    website = db.Column(db.String())
    country = db.Column(db.String())
    industry = db.Column(db.Integer())
    sector = db.Column(db.String())
    longBusinessSummary = db.Column(db.String())
    fullTimeEmployees = db.Column(db.Integer())

    # price
    price = db.Column(db.Float())
    price_open = db.Column(db.Float())
    regularMarketVolume = db.Column(db.Float())
    regularMarketDayLow = db.Column(db.Float())
    regularMarketDayHigh = db.Column(db.Float())
    dayLow = db.Column(db.Float())
    dayHigh = db.Column(db.Float())
    trailingPE = db.Column(db.Float())
    forwardPE = db.Column(db.Float())
    volume = db.Column(db.Float())
    averageVolume = db.Column(db.Float())
    averageVolume10days = db.Column(db.Float())
    bid = db.Column(db.Float())
    ask = db.Column(db.Float())
    bidSize = db.Column(db.Float())
    askSize = db.Column(db.Float())
    marketCap = db.Column(db.Float())
    fiftyTwoWeekLow = db.Column(db.Float())
    fiftyTwoWeekHigh = db.Column(db.Float())
    fiftyDayAverage = db.Column(db.Float())
    twoHundredDayAverage = db.Column(db.Float())

    # dividend
    dividend_rate = db.Column(db.Float())
    dividendYield = db.Column(db.Float())
    exDividendDate = db.Column(db.String())
    trailingAnnualDividendRate = db.Column(db.Float())
    trailingAnnualDividendYield = db.Column(db.Float())
    fiveYearAvgDividendYield = db.Column(db.Float())

    # financial_data
    totalCash = db.Column(db.Float())
    totalCashPerShare = db.Column(db.Float())
    totalDebt = db.Column(db.Float())
    totalRevenue = db.Column(db.Float())
    debtToEquity = db.Column(db.Float())
    revenuePerShare = db.Column(db.Float())
    freeCashflow = db.Column(db.Float())
    operatingCashflow = db.Column(db.Float())
    earningsGrowth = db.Column(db.Float())
    revenueGrowth = db.Column(db.Float())
    currency = db.Column(db.String())

    # recommendation trend
    recommendation_trend = db.Column(db.String())
    targetHighPrice = db.Column(db.Float())
    targetLowPrice = db.Column(db.Float())
    targetMeanPrice = db.Column(db.Float())
    targetMedianPrice = db.Column(db.Float())
    recommendationMean = db.Column(db.Float())
    recommendationKey = db.Column(db.String())
    numberOfAnalystOpinions = db.Column(db.Integer)

    # other
    earnings = db.Column(db.String())
    history = db.Column(db.String())
    filings = db.Column(db.String())
    ownershipList = db.Column(db.String())

    def to_dict(self):
        data = {
            'id': self.id,
            'symbol': self.symbol,
            'name': self.name,
            'website': self.website,
            'country': self.country,
            'industry': self.industry,
            'sector': self.sector,
            'longBusinessSummary': self.longBusinessSummary,
            'fullTimeEmployees': self.fullTimeEmployees,
            'regularMarketPrice': self.price,
            'regularMarketOpen': self.price_open,
            'regularMarketVolume': self.regularMarketVolume,
            'regularMarketDayLow': self.regularMarketDayLow,
            'regularMarketDayHigh': self.regularMarketDayHigh,
            'dayLow': self.dayLow,
            'dayHigh': self.dayHigh,
            'trailingPE': self.trailingPE,
            'forwardPE': self.forwardPE,
            'volume': self.volume,
            'averageVolume': self.averageVolume,
            'averageVolume10days': self.averageVolume10days,
            'bid': self.bid,
            'ask': self.ask,
            'bidSize': self.bidSize,
            'askSize': self.askSize,
            'marketCap': self.marketCap,
            'fiftyTwoWeekLow': self.fiftyTwoWeekLow,
            'fiftyTwoWeekHigh': self.fiftyTwoWeekHigh,
            'fiftyDayAverage': self.fiftyDayAverage,
            'twoHundredDayAverage': self.twoHundredDayAverage,
            'dividend_rate': self.dividend_rate,
            'dividendYield': self.dividendYield,
            'exDividendDate': self.exDividendDate,
            'trailingAnnualDividendRate': self.trailingAnnualDividendRate,
            'trailingAnnualDividendYield': self.trailingAnnualDividendYield,
            'fiveYearAvgDividendYield': self.fiveYearAvgDividendYield,
            'totalCash': self.totalCash,
            'totalCashPerShare': self.totalCashPerShare,
            'totalDebt': self.totalDebt,
            'totalRevenue': self.totalRevenue,
            'debtToEquity': self.debtToEquity,
            'revenuePerShare': self.revenuePerShare,
            'freeCashflow': self.freeCashflow,
            'operatingCashflow': self.operatingCashflow,
            'earningsGrowth': self.earningsGrowth,
            'revenueGrowth': self.revenueGrowth,
            'currency': self.currency,
            'recommendation_trend': self.recommendation_trend,
            'targetHighPrice': self.targetHighPrice,
            'targetLowPrice': self.targetLowPrice,
            'targetMeanPrice': self.targetMeanPrice,
            'targetMedianPrice': self.targetMedianPrice,
            'recommendationMean': self.recommendationMean,
            'recommendationKey': self.recommendationKey,
            'numberOfAnalystOpinions': self.numberOfAnalystOpinions,
            'history': self.history,
        }
        return data

    def __repr__(self):
        return '<Stock_data {}>'.format(self.to_dict())


class Etf_data(db.Model):
    # general
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.Integer, db.ForeignKey('asset.symbol'), unique=True)
    name = db.Column(db.String())

    price = db.Column(db.Float())
    price_open = db.Column(db.Float())
    regularMarketVolume = db.Column(db.Float())
    regularMarketDayLow = db.Column(db.Float())
    regularMarketDayHigh = db.Column(db.Float())
    dividend_rate = db.Column(db.Float())

    def to_dict(self):
        data = {
            'symbol': self.symbol,
            'name': self.name,
            'price': self.price,
            'price_open': self.price_open,
            'regularMarketVolume': self.regularMarketVolume,
            'regularMarketDayLow': self.regularMarketDayLow,
            'regularMarketDayHigh': self.regularMarketDayHigh,
            'dividend_rate': self.dividend_rate,
        }
        return data

    def __repr__(self):
        return '<Etf_data {}>'.format(self.to_dict())


class Crypto_data(db.Model):
    # general
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.Integer, db.ForeignKey('asset.symbol'), unique=True)
    name = db.Column(db.String())

    price = db.Column(db.Float())
    price_open = db.Column(db.Float())
    regularMarketVolume = db.Column(db.Float())
    regularMarketDayLow = db.Column(db.Float())
    regularMarketDayHigh = db.Column(db.Float())

    def to_dict(self):
        data = {
            'symbol': self.symbol,
            'name': self.name,
            'price': self.price,
            'price_open': self.price_open,
            'regularMarketVolume': self.regularMarketVolume,
            'regularMarketDayLow': self.regularMarketDayLow,
            'regularMarketDayHigh': self.regularMarketDayHigh,
        }
        return data

    def __repr__(self):
        return '<Crypto_data {}>'.format(self.to_dict())


class Asset_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))
