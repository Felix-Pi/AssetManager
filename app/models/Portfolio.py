from datetime import datetime

from app import db, app
from app.models.Asset import *
from app.models.Portfolio_position import Portfolio_positions


class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, db.ForeignKey('portfolio_types.id'))
    type_str = db.relationship("Portfolio_types")

    title = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    positions_db = db.relationship("Portfolio_positions", lazy='dynamic')
    transactions = db.relationship("Transaction", lazy='dynamic')
    value = db.Column(db.String(64))

    @orm.reconstructor
    def init_on_load(self):
        self.positions = self.get_positions()
        self.value = self.calc_portfolio_value()

    def to_dict(self):
        data = {
            'type': self.type,
            'title': self.title,
            'user_id': self.user_id,
            'positions': self.positions,
            'transactions': [t.to_dict() for t in self.transactions.all()],
        }
        return data

    def __repr__(self):
        return '<Portfolio {}>'.format(self.to_dict())

    @staticmethod
    def get_portfolio(id):
        return db.session.query(Portfolio).filter_by(id=id).first()

    def remove_transaction(self, id):
        pass

    def get_positions(self):
        positions = self.positions_db.all()
        res = []

        for position in positions:
            res.append(position.get_data())

        return res

    def update_position(self, symbol):
        transactions = db.session.query(Transaction).filter_by(symbol=symbol, portfolio_id=self.id) \
            .all()


        data = {
            'quantity': 0,
            'buyin': 0,
            'value': 0,
            'transactions_above_zero': 0,
        }
        for transaction in transactions:
            type = transaction.type
            quantity = float(transaction.quantity)

            price = float(transaction.price)

            if type == 1:  # buy
                data['quantity'] += quantity
                data['transactions_above_zero'] += 1
                data['buyin'] = round((data['buyin'] + price) / data['transactions_above_zero'], 2)

            if type == 2:  # sell
                data['quantity'] -= quantity

                if data['quantity'] == 0:
                    data['buyin'] = 0
                    data['transactions_above_zero'] = 0

        data['value'] = round(data['quantity'] * Asset.get_symbol(symbol).price, 2)

        position = db.session.query(Portfolio_positions).filter_by(portfolio=self.id, symbol=symbol).first()

        if position is None:
            position = Portfolio_positions(portfolio=self.id, symbol=symbol, quantity=data['quantity'],
                                           value=data['value'], buyin=data['buyin'])

            db.session.add(position)
        else:
            position.quantity = data['quantity']
            position.value = data['value']
            position.buyin = data['buyin']


        db.session.commit()

        self.value = self.calc_portfolio_value()

        return position

    def add_transaction_(self, symbol, type, timestamp, price, quantity):
        transaction = Transaction(portfolio_id=self.id, symbol=symbol, type=type, timestamp=timestamp, price=price,
                                  quantity=quantity)

        db.session.add(transaction)
        db.session.commit()

        self.update_position(symbol)

        return transaction

    @staticmethod
    def add_transaction(portfolio_id, symbol, timestamp, type, price, quantity):
        portfolio = Portfolio.get_portfolio(portfolio_id)

        portfolio.add_transaction_(symbol, type, timestamp, price, quantity)

    def calc_portfolio_value(self):
        return round(sum(pos['value'] for pos in self.positions), 2)

    def calc_portfolio_profit(self):
        total_absolute = sum(pos['profit']['total_absolute'] for pos in self.positions)
        total_relative = total_absolute / self.value * 100
        today_absolute = sum(pos['profit']['today_absolute'] for pos in self.positions)
        today_relative = today_absolute / self.value * 100

        data = {
            'today_absolute': round(today_absolute, 2),
            'today_relative': round(today_relative, 2),
            'total_absolute': round(total_absolute, 2),
            'total_relative': round(total_relative, 2),
        }

        return data

    def calc_dividend(self):
        return round(sum(pos['dividend'] for pos in self.positions if 'dividend' in pos), 2)

    def calc_stock_distribution(self):
        doughnut_asset_allocation = sorted(self.positions, key=lambda k: k['value'], reverse=True)

        return {
            'data_relative': [round((asset['value'] / self.value) * 100, 1) for asset in
                              doughnut_asset_allocation],
            'data_absolute': [asset['value'] for asset in doughnut_asset_allocation],
            'labels': [asset['symbol'] for asset in doughnut_asset_allocation],
        }

    def calc_sector_distribution(self):
        data = {}
        for pos in self.positions:
            sector = pos['industry']
            value = pos['value']

            if sector not in data:
                data[sector] = {'total': value, 'relative': value / self.value * 100}
            else:
                data[sector]['total'] += value
                data[sector]['relative'] = data[sector]['total'] / self.value * 100

        data = dict(sorted(data.items(), key=lambda t: t[1]['total'], reverse=True))

        return {'data_relative': [data[key]['relative'] for key in data],
                'data_absolute': [data[key]['total'] for key in data],
                'labels': [key for key in data]}

    def calc_country_distribution(self):
        data = {}
        for pos in self.positions:
            country = pos['country']
            value = pos['value']

            if country not in data:
                data[country] = {'total': value, 'relative': value / self.value * 100}
            else:
                data[country]['total'] += value
                data[country]['relative'] = data[country]['total'] / self.value * 100

        data = dict(sorted(data.items(), key=lambda t: t[1]['total'], reverse=True))

        return {'data_relative': [data[key]['relative'] for key in data],
                'data_absolute': [data[key]['total'] for key in data],
                'labels': [key for key in data]}


    def update_portfolio_positions(self):
        for pos in self.positions:
            self.update_position(pos['symbol'])

        self.value = self.calc_portfolio_value()

    @staticmethod
    def update_all_portfolio_positions():
        portfolios = db.session.query(Portfolio).all()

        app.logger.info('Updating positions for  \'{}\' Portfolios'.format(len(portfolios)))
        for pf in portfolios:
            pf.update_portfolio_positions()




class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'))
    symbol = db.Column(db.Integer, db.ForeignKey('asset.symbol'))
    type = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    price = db.Column(db.Float())
    quantity = db.Column(db.Float())

    def get_data(self):
        return {}

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'portfolio_id': self.portfolio_id,
            'symbol': self.symbol,
            'type': self.type,
            'timestamp': self.timestamp,
            'price': self.price,
            'quantity': self.quantity,
        }
        return data

    def __repr__(self):
        return '<Transaction {}>'.format(self.to_dict())


class Portfolio_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'type': self.type,
        }
        return data

    def __repr__(self):
        return '<Portfolio_type {}>'.format(self.to_dict())


if __name__ == '__main__':
    Portfolio(type=1, )
