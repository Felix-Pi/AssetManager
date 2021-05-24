from datetime import datetime

from sqlalchemy import orm

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

    value = db.Column(db.Float, default=0)
    profit_today_rel = db.Column(db.Float, default=0)
    profit_today_abs = db.Column(db.Float, default=0)
    profit_total_rel = db.Column(db.Float, default=0)
    profit_total_abs = db.Column(db.Float, default=0)

    expected_dividend = db.Column(db.Float, default=0)

    @orm.reconstructor
    def init_on_load(self):
        self.positions = self.get_positions()
        self.calc_position_counter = 0

    def update_value(self, commit=False):
        self.value = round(sum(pos.value for pos in self.positions), 2)

        if commit:
            db.session.commit()

    def update_profit(self, commit=True):
        try:
            self.profit_total_abs = round(sum(pos.profit_total_abs for pos in self.positions), 2)
            self.profit_total_rel = round(self.profit_total_abs / self.value * 100, 2)
            self.profit_today_abs = round(sum(pos.profit_today_abs for pos in self.positions), 2)
            self.profit_today_rel = round(self.profit_today_abs / self.value * 100, 2)

            if commit:
                db.session.commit()

        except ZeroDivisionError:
            app.logger.error('update_profit: Error occured for portfolio\'{}\': ZeroDivisionError'.format(self.title))
        except Exception:
            app.logger.error('update_profit: Error occured for portfolio \'{}\''.format(self.title))

    def calc_expected_dividend(self, commit=False):
        self.expected_dividend = round(sum(pos.expected_dividend for pos in self.positions), 2)

    def calc_stock_distribution(self):
        doughnut_asset_allocation = sorted(self.positions, key=lambda k: k.value, reverse=True)

        return {
            'data_relative': [round((asset.value / self.value) * 100, 1) for asset in
                              doughnut_asset_allocation],
            'data_absolute': [asset.value for asset in doughnut_asset_allocation],
            'labels': [asset.symbol for asset in doughnut_asset_allocation],
        }

    def calc_sector_distribution(self):
        data = {}
        for pos in self.positions:
            sector = pos.symbol_elem.sector
            value = pos.value

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
            industry = pos.symbol_elem.industry
            value = pos.value

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
            industry = pos.symbol_elem.country
            value = pos.value

            if industry not in data:
                data[industry] = {'total': value, 'relative': value / self.value * 100}
            else:
                data[industry]['total'] += value
                data[industry]['relative'] = data[industry]['total'] / self.value * 100

        data = dict(sorted(data.items(), key=lambda t: t[1]['total'], reverse=True))

        return {'data_relative': [data[key]['relative'] for key in data],
                'data_absolute': [data[key]['total'] for key in data],
                'labels': [key for key in data]}

    def get_positions(self):
        data = self.positions_db.filter(Portfolio_positions.quantity > 0).order_by(
            Portfolio_positions.value.desc()).all()

        return data

    def update_portfolio_positions(self, log=False):
        if log:
            app.logger.info('Updating Portfolio Positions for \'{}\': '.format(self.title))

        for pos in self.positions:
            self.update_position(pos.symbol, log=True)

    def calc_position(self, symbol, transactions=None, until_data=None):
        self.calc_position_counter += 1

        if transactions is not None:
            transactions = list(filter(lambda x: x.symbol == symbol, transactions))
        else:
            transactions = db.session.query(Transaction).filter_by(symbol=symbol, portfolio_id=self.id).all()
        if until_data is not None:
            transactions = list(filter(lambda x: x.timestamp <= until_data.replace(tzinfo=None), transactions))

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

        return data

    def update_position(self, symbol, log=False):
        if log:
            app.logger.info('Updating Position for  \'{}\' in \'{}\': '.format(symbol, self.title))
        data = self.calc_position(symbol)

        position = db.session.query(Portfolio_positions).filter_by(portfolio=self.id, symbol=symbol).first()

        if position is None:
            position = Portfolio_positions(portfolio=self.id, symbol=symbol)

            db.session.add(position)

        position.quantity = data['quantity']
        position.buyin = data['buyin']

        position.update_value(commit=False)
        position.update_profit(commit=False)
        position.update_expected_dividend(commit=False)
        position.update_portfolio_percentage(commit=False)

        db.session.commit()

        self.positions = self.get_positions()

        self.update_value()
        self.update_profit()

        db.session.commit()

        return position

    def add_transaction(self, symbol, type, timestamp, price, quantity, fee=None):
        if fee is None:
            if type == 1 or type == 2:
                fee = 1.0
            if type == 3 or type == 4 or type == 5:
                fee = 0.0

        if type == 4:  # money transfer #todo needed?
            transaction = Transaction(portfolio_id=self.id, symbol=None, type=type, timestamp=timestamp, price=price,
                                      quantity=quantity, cost=fee)
        else:
            transaction = Transaction(portfolio_id=self.id, symbol=symbol, type=type, timestamp=timestamp, price=price,
                                      quantity=quantity, cost=fee)

        db.session.add(transaction)
        db.session.commit()

        if type != 4:
            self.update_position(symbol)
            self.update_value()
            self.update_profit()

        return transaction

    def remove_transaction(self, id):
        pass

    def to_dict(self):
        data = {
            'type': self.type,
            'title': self.title,
            'user_id': self.user_id,
            'value': self.value,
            'profit': self.profit,
            'profit_today_abs': self.profit_today_abs,
            'profit_total_rel': self.profit_total_rel,
            'profit_total_abs': self.profit_total_abs,
            'profit_today_rel': self.profit_today_rel,
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
    suffix = db.Column(db.String(64))
    sort = db.Column(db.Integer)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'title': self.title,
            'suffix': self.suffix,
            'sort': self.sort,
        }
        return data

    def __repr__(self):
        return '<Transaction_type {}>'.format(self.to_dict())


class Portfolio_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))

    def to_dict(self):
        data = {
            'id': self.id,
            'type': self.type,
        }
        return data

    def __repr__(self):
        return '<Portfolio_type {}>'.format(self.to_dict())


if __name__ == '__main__':
    Portfolio(type=1, )
