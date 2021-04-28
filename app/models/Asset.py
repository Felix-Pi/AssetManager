import json
import re
from datetime import datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy import orm

from app import db


class Asset(db.Model):
    symbol = db.Column(db.String(64), primary_key=True, unique=True)
    alternative_symbol = db.Column(db.String(64))
    title = db.Column(db.String(64))
    type = db.Column(db.Integer, db.ForeignKey('asset_types.id'))
    type_str = db.relationship("Asset_types")
    price = db.Column(db.Integer)
    price_open = db.Column(db.Integer)
    asset_data_id = db.Column(db.Integer)

    @orm.reconstructor
    def init_on_load(self):
        self.data = self.get_data()

        if isinstance(self.data, dict) is False:
            self.data = self.data.to_dict()

            for d in self.data:
                setattr(self, d, self.data[d])

    def get_data(self):
        data = {}
        if self.type == 1:
            data = db.session.query(Stock_data).filter_by(symbol=self.symbol).first()
        if self.type == 2:
            data = db.session.query(Etf_data).filter_by(symbol=self.symbol).first()
        if self.type == 3:
            data = db.session.query(Crypto_data).filter_by(symbol=self.symbol).first()

        return data

    def get_property(self, property):
        if hasattr(self, property):
            attr = getattr(self, property)
            if attr is not None:
                return attr
        return '-'

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

    def parse_earnings(self):
        return self.earnings

    def to_dict(self):
        data = {
            'title': self.title,
            'symbol': self.symbol,
            'alternative_symbol': self.alternative_symbol,
            'type': self.type,
            'price': self.price,
            'price_open': self.price_open,
            'asset_data_id': self.asset_data_id,
            # 'data': self.data,
            # 'data': self.data if hasattr(self, 'data') else self.get_data(),
        }

        if hasattr(self, 'data'):
            for d in self.data:
                data[d] = self.data[d]

        return data

    def __repr__(self):
        return '<Asset {}>'.format(self.to_dict())


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
    exchange = db.Column(db.String(64))
    exchange_name = db.Column(db.String(64))
    quote_type = db.Column(db.String(64))
    underlying_symbol = db.Column(db.String(64))

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
    ex_dividend_date = db.Column(db.String())
    dividend_date = db.Column(db.String())

    history = db.Column(db.String())
    filings = db.Column(db.String())
    ownershipList = db.Column(db.String())

    def to_dict(self):
        data = {}
        blacklist = ['__abstract__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__',
                     '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__',
                     '__le__', '__lt__', '__mapper__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
                     '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__table__',
                     '__tablename__', '__weakref__', '_sa_class_manager', '_sa_instance_state', '_sa_registry']

        attributes = dir(self)

        for attr in attributes:
            if attr not in blacklist:
                if hasattr(self, attr):
                    data[attr] = getattr(self, attr)

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
        data = {}
        blacklist = ['__abstract__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__',
                     '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__',
                     '__le__', '__lt__', '__mapper__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
                     '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__table__',
                     '__tablename__', '__weakref__', '_sa_class_manager', '_sa_instance_state', '_sa_registry']

        attributes = dir(self)

        for attr in attributes:
            if attr not in blacklist:
                data[attr] = getattr(self, attr)

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
        data = {}
        blacklist = ['__abstract__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__',
                     '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__',
                     '__le__', '__lt__', '__mapper__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
                     '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__table__',
                     '__tablename__', '__weakref__', '_sa_class_manager', '_sa_instance_state', '_sa_registry']

        attributes = dir(self)

        for attr in attributes:
            if attr not in blacklist:
                data[attr] = getattr(self, attr)

        return data

    def __repr__(self):
        return '<Crypto_data {}>'.format(self.to_dict())


class Currency_data(db.Model):
    # general
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.Integer, db.ForeignKey('asset.symbol'), unique=True)

    price = db.Column(db.Float())
    price_open = db.Column(db.Float())
    title = db.Column(db.String(64))

    def to_dict(self):
        data = {}
        blacklist = ['__abstract__', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__',
                     '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__',
                     '__le__', '__lt__', '__mapper__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__',
                     '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__table__',
                     '__tablename__', '__weakref__', '_sa_class_manager', '_sa_instance_state', '_sa_registry']

        attributes = dir(self)

        for attr in attributes:
            if attr not in blacklist:
                data[attr] = getattr(self, attr)

        return data

    def __repr__(self):
        return '<Crypto_data {}>'.format(self.to_dict())


class Asset_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))
