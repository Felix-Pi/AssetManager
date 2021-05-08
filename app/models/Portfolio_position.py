from app import db
from app.models.Portfolio import *


class Portfolio_positions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    portfolio = db.Column(db.Integer, db.ForeignKey('portfolio.id'))
    portfolio_elem = db.relationship('Portfolio', viewonly=True)
    symbol = db.Column(db.String, db.ForeignKey('asset.symbol'))
    symbol_elem = db.relationship('Asset')

    quantity = db.Column(db.Float)
    value = db.Column(db.Float)
    buyin = db.Column(db.Float)

    @orm.reconstructor
    def init_on_load(self):
        self.value = self.calc_value()
        self.profit = self.calc_profit()
        self.dividend = self.calc_expected_dividend()
        self.portfolio_percentage = self.calc_portfolio_percentage()

    def get_data(self):
        data = db.session.query(Portfolio_positions, Asset) \
            .join(Asset, Asset.symbol == Portfolio_positions.symbol) \
            .filter(Asset.symbol == self.symbol).first()

        res = {}
        for elem in data:
            res.update(elem.to_dict())

        return res

    def calc_value(self):
        if self.symbol_elem is None:
            self.symbol_elem = db.session.query(Asset).filter(Asset.symbol == self.symbol).first()
        return round(self.quantity * self.symbol_elem.price, 2)

    def calc_profit(self):
        price_open = self.symbol_elem.price_open
        value = self.value

        try:
            total_absolute = value - (self.quantity * self.buyin)

            today_relative = total_absolute / value * 100
            today_absolute = value - (self.quantity * price_open)
            total_relative = today_absolute / self.value * 100

            data = {
                'today_absolute': round(today_absolute, 2),
                'today_relative': round(today_relative, 2),
                'total_absolute': round(total_absolute, 2),
                'total_relative': round(total_relative, 2),
            }
            return data
        except ZeroDivisionError:
            return {
                'today_absolute': 0,
                'today_relative': 0,
                'total_absolute': 0,
                'total_relative': 0,
            }

    def calc_portfolio_percentage(self):
        if self.portfolio_elem is None or self.portfolio_elem.value == 0:
            return 0
        return round(self.value / self.portfolio_elem.value, 2)

    def calc_expected_dividend(self):
        if self.symbol_elem.type == 1 or self.symbol_elem.type == 2:
            dividend_rate = self.symbol_elem.dividend

            if dividend_rate is None:
                dividend_rate = 0

            return self.quantity * dividend_rate
        return 0

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

        if hasattr(self, 'symbol_elem'):
            data['name'] = self.symbol_elem.name
        return data

    def __repr__(self):
        return '<Portfolio_positions {}>'.format(self.to_dict())
