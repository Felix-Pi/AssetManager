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
        self.dividend = self.calc_dividend()
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

        total_absolute = self.value - (self.quantity * self.buyin)

        today_relative = total_absolute / self.value * 100
        today_absolute = self.value - (self.quantity * price_open)
        total_relative = today_absolute / self.value * 100

        data = {
            'today_absolute': round(today_absolute, 2),
            'today_relative': round(today_relative, 2),
            'total_absolute': round(total_absolute, 2),
            'total_relative': round(total_relative, 2),
        }
        return data

    def calc_portfolio_percentage(self):
        if self.portfolio_elem is None or self.portfolio_elem.value == 0:
            return 0
        return round(self.value / self.portfolio_elem.value, 2)

    def calc_dividend(self):
        if self.symbol_elem.type == 1 or self.symbol_elem.type == 2:
            dividend_rate = self.symbol_elem.dividend_rate

            if dividend_rate is None:
                dividend_rate = 0

            return self.quantity * dividend_rate
        return 0

    def to_dict(self):
        data = {
            'portfolio': self.portfolio,
            'symbol': self.symbol,
            'title': self.symbol_elem.title,
            'symbol_elem': self.symbol_elem,  # todo delete?
            'quantity': self.quantity,
            'value': self.value,
            'buyin': self.buyin,
            'profit': self.profit,
            'portfolio_percentage': self.portfolio_percentage,
            'dividend': self.dividend,
        }
        return data

    def __repr__(self):
        return '<Portfolio_positions {}>'.format(self.to_dict())
