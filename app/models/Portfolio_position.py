from app import db
from app.models.Portfolio import *


class Portfolio_positions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    portfolio = db.Column(db.Integer, db.ForeignKey('portfolio.id'))
    symbol = db.Column(db.String, db.ForeignKey('asset.symbol'))

    quantity = db.Column(db.Float)
    value = db.Column(db.Float)
    buyin = db.Column(db.Float)

    def to_dict(self):
        data = {
            'portfolio': self.portfolio,
            'symbol': self.symbol,
            'symbol_elem': self.symbol,
            'quantity': self.quantity,
            'value': self.value,
            'buyin': self.buyin,
            'profit': self.calc_profit(),
            'portfolio_percentage': self.calc_portfolio_percentage(),
            'dividend': self.calc_dividend(),
        }
        return data

    def __repr__(self):
        return '<Portfolio_positions {}>'.format(self.to_dict())

    def get_portfolio(self):
        return db.session.query(Portfolio).filter_by(id=self.portfolio).first()

    def get_data(self):
        data = db.session.query(Portfolio_positions, Asset) \
            .join(Asset, Asset.symbol == Portfolio_positions.symbol) \
            .filter(Asset.symbol == self.symbol).first()

        res = {}
        for elem in data:
            res.update(elem.to_dict())

        return res

    def calc_profit(self):
        symbol_elem = Asset.get_symbol(self.symbol)

        price_open = symbol_elem.price_open

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
        # return round(self.value / portfolio_value, 2)
        return 1  # todo

    def calc_dividend(self):
        symbol_elem = Asset.get_symbol(self.symbol)

        if symbol_elem.type == 1 or symbol_elem.type == 2:
            dividend_rate = symbol_elem.dividend_rate

            if dividend_rate is None:
                dividend_rate = 0

            return self.quantity * dividend_rate
        return 0
