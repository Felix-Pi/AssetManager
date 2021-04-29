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
    transactions = db.relationship("Transaction", lazy='dynamic', order_by="desc(Transaction.timestamp)")
    positions_db = db.relationship("Portfolio_positions", lazy='dynamic')
    value = db.Column(db.Float)

    @orm.reconstructor
    def init_on_load(self):
        self.positions = self.get_positions()
        self.value = self.calc_value()
        self.profit = self.calc_profit()

    def calc_value(self):
        return round(sum(pos['value'] for pos in self.positions), 2)

    def calc_profit(self):
        if self.value == 0 or self.value is None:
            self.value = 0.00000001

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
            sector = pos['sector']
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

    def calc_industry_distribution(self):
        data = {}
        for pos in self.positions:
            industry = pos['industry']
            value = pos['value']

            if industry not in data:
                data[industry] = {'total': value, 'relative': value / self.value * 100}
            else:
                data[industry]['total'] += value
                data[industry]['relative'] = data[industry]['total'] / self.value * 100

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

    def get_positions(self):
        positions = self.positions_db.filter(Portfolio_positions.quantity > 0).order_by(
            Portfolio_positions.value.desc()).all()
        result = []

        for position in positions:
            if position.quantity > 0:
                result.append(position.get_data())

        return result

    def update_portfolio_positions(self, log=False):
        if log:
            app.logger.info('Updating Portfolio Positions for \'{}\': '.format(self.title))

        for pos in self.positions:
            self.update_position(pos['symbol'])

    def update_position(self, symbol):
        transactions = db.session.query(Transaction).filter_by(symbol=symbol, portfolio_id=self.id) \
            .all()

        data = {
            'quantity': 0,
            'buyin': 0,
            'value': 0,
        }

        for transaction in transactions:
            type = transaction.type

            if type == 1 or type == 2 or type == 3:  # buy, sell, monthly
                quantity = float(transaction.quantity)
                price = float(transaction.price)

                if type == 1 or type == 3:  # buy, monthly
                    data['quantity'] += quantity
                    data['buyin'] += (price * quantity)

                if type == 2:  # sell
                    data['quantity'] -= quantity
                    data['buyin'] -= (price * quantity)

                    if data['quantity'] == 0:
                        data['buyin'] = 0

        if data['buyin'] != 0:
            data['buyin'] = round(data['buyin'] / data['quantity'], 7)

        data['quantity'] = round(data['quantity'], 7)

        position = db.session.query(Portfolio_positions).filter_by(portfolio=self.id, symbol=symbol).first()

        if position is None:
            position = Portfolio_positions(portfolio=self.id, symbol=symbol, quantity=data['quantity'],
                                           buyin=data['buyin'])

            position.value = position.calc_value()
            position.profit = position.calc_profit()
            position.dividend = position.calc_dividend()
            position.portfolio_percentage = position.calc_portfolio_percentage()
            db.session.add(position)
        else:
            position.quantity = data['quantity']
            position.buyin = data['buyin']
            position.value = position.calc_value()
            position.profit = position.calc_profit()
            position.dividend = position.calc_dividend()
            position.portfolio_percentage = position.calc_portfolio_percentage()

        db.session.commit()

        self.positions = self.get_positions()
        self.value = self.calc_value()
        db.session.commit()

        return position

    def add_transaction(self, symbol, type, timestamp, price, quantity, cost=None):
        if cost is None:
            if type == 1 or type == 2:
                cost = 1.0
            if type == 3 or type == 4 or type == 5:
                cost = 0.0

        if type == 4:  # money transfer
            transaction = Transaction(portfolio_id=self.id, symbol=None, type=type, timestamp=timestamp, price=price,
                                      quantity=quantity, cost=cost)
        else:
            transaction = Transaction(portfolio_id=self.id, symbol=symbol, type=type, timestamp=timestamp, price=price,
                                      quantity=quantity, cost=cost)

        db.session.add(transaction)
        db.session.commit()

        if type != 4:
            self.update_position(symbol)

        return transaction

    def remove_transaction(self, id):
        pass

    def to_dict(self):
        data = {
            'type': self.type,
            'title': self.title,
            'user_id': self.user_id,
            'positions': self.positions,
            'profit': self.profit,
            'value': self.value,
            'transactions': [t.to_dict() for t in self.transactions.all()],
        }
        return data

    def __repr__(self):
        return '<Portfolio {}>'.format(self.to_dict())


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolio.id'))
    symbol = db.Column(db.Integer, db.ForeignKey('asset.symbol'))
    type = db.Column(db.Integer, db.ForeignKey('transaction_types.id'))
    type_str = db.relationship("Transaction_types")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    price = db.Column(db.Float())
    quantity = db.Column(db.Float())
    cost = db.Column(db.Float())

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'portfolio_id': self.portfolio_id,
            'symbol': self.symbol,
            'type': self.type,
            'type_str': self.type_str,
            'timestamp': self.timestamp,
            'price': self.price,
            'quantity': self.quantity,
        }
        return data

    def __repr__(self):
        return '<Transaction {}>'.format(self.to_dict())


class Transaction_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'title': self.title,
        }
        return data

    def __repr__(self):
        return '<Transaction_type {}>'.format(self.to_dict())


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
