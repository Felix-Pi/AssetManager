from app import db, app
from app.models.Portfolio import *


class Portfolio_positions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    portfolio = db.Column(db.Integer, db.ForeignKey('portfolio.id'))
    portfolio_elem = db.relationship('Portfolio', viewonly=True)
    symbol = db.Column(db.String, db.ForeignKey('asset.symbol'))
    symbol_elem = db.relationship('Asset')

    quantity = db.Column(db.Float, default=0)
    value = db.Column(db.Float, default=0)
    buyin = db.Column(db.Float, default=0)
    price_open = db.Column(db.Float, default=0)

    profit_today_rel = db.Column(db.Float, default=0)
    profit_today_abs = db.Column(db.Float, default=0)
    profit_total_rel = db.Column(db.Float, default=0)
    profit_total_abs = db.Column(db.Float, default=0)

    expected_dividend = db.Column(db.Float, default=0)
    portfolio_percentage = db.Column(db.Float, default=0)

    def get_data(self):
        data = db.session.query(Portfolio_positions, Asset) \
            .join(Asset, Asset.symbol == Portfolio_positions.symbol) \
            .filter(Asset.symbol == self.symbol).first()

        res = {}
        for elem in data:
            res.update(elem.to_dict())

        return res

    def update_value(self, commit=False):
        value = 0
        try:
            if self.symbol_elem is None:
                self.symbol_elem = db.session.query(Asset).filter(Asset.symbol == self.symbol).first()

            value = round(self.quantity * self.symbol_elem.price, 2)
        except Exception:
            app.logger.error('update_value: Error occured for symbol {}'.format(self.symbol))
            return value

        self.value = value
        if commit:
            db.session.commit()

    def update_profit(self, commit=False):
        self.update_value(commit=False)
        try:
            self.price_open = self.symbol_elem.price_open

            self.profit_total_abs = round(self.value - (self.quantity * self.buyin), 2)
            self.profit_total_rel = round(self.profit_total_abs / self.value * 100, 2)
            self.profit_today_abs = round(self.value - (self.quantity * self.price_open), 2)
            self.profit_today_rel = round(self.profit_today_abs / self.value * 100, 2)

        except ZeroDivisionError:
            app.logger.error('calc_profit: Error occured for symbol \'{}\': ZeroDivisionError'.format(self.symbol))
        except Exception as err:
            app.logger.error('calc_profit: Error occured for symbol \'{}\''.format(self.symbol))
            app.logger.error('calc_profit: Error occured for symbol \'{}\': {}'.format(self.symbol, err))

        if commit:
            db.session.commit()

    def calc_profit(self):
        self.update_profit()

        return {
            'today_absolute': self.profit_today_abs,
            'today_relative': self.profit_today_rel,
            'total_absolute': self.profit_total_abs,
            'total_relative': self.profit_total_rel
        }

    def update_portfolio_percentage(self, commit=False):
        self.portfolio_percentage = 0
        if self.portfolio_elem is not None and self.portfolio_elem.value != 0:
            self.portfolio_percentage = round(self.value / self.portfolio_elem.value, 2)

        if commit:
            db.session.commit()

    def update_expected_dividend(self, commit=False):
        expected_dividend = 0
        if self.symbol_elem.type == 1 or self.symbol_elem.type == 2:
            dividend_rate = self.symbol_elem.dividend

            if dividend_rate is None:
                dividend_rate = 0

            expected_dividend = self.quantity * dividend_rate

        self.expected_dividend = expected_dividend

        if commit:
            db.session.commit()

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

    def to_dict(self):
        data = {
            'id': self.id,
            'portfolio': self.portfolio,
            'symbol': self.symbol,
            'symbol_elem': self.symbol_elem,
            'quantity': self.quantity,
            'value': self.value,
            'buyin': self.buyin,

        }
        return data

    def __repr__(self):
        return '<Portfolio_positions {}>'.format(self.to_dict())
