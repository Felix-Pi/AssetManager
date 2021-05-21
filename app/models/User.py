from datetime import time, datetime, timedelta
from hashlib import md5

import jwt as jwt
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import login, db, app


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    portfolios = db.relationship("Portfolio", backref='user', lazy='dynamic')

    networth = db.Column(db.Float, default=0)
    expected_dividend = db.Column(db.Float, default=0)
    profit_today_rel = db.Column(db.Float, default=0)
    profit_today_abs = db.Column(db.Float, default=0)
    profit_total_rel = db.Column(db.Float, default=0)
    profit_total_abs = db.Column(db.Float, default=0)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def get_name(self):
        return self.prename + ' ' + self.surname

    def update_networth(self, commit=False):
        self.networth = round(sum([pf.value for pf in self.portfolios.all()]), 2)

        if commit:
            db.session.commit()

    def update_profit(self, commit=False):
        self.update_networth()

        self.profit_total_abs = round(
            sum([pf.profit_total_rel for pf in self.portfolios.all()]), 2)
        self.profit_today_abs = round(
            sum([pf.profit_today_abs for pf in self.portfolios.all()]), 2)

        self.profit_total_rel = round(self.profit_total_rel / self.networth * 100, 2)
        self.profit_today_rel = round(self.profit_today_abs / self.networth * 100, 2)

        if commit:
            db.session.commit()

    def update_expected_dividend(self, commit=False):
        self.expected_dividend = sum([pf.expected_dividend for pf in self.portfolios.all()])

        if commit:
            db.session.commit()

    def get_all_transactions(self, sort_by='timestamp', sort_reverse=True, calc_meta=False):
        def calc_meta(meta, tr):
            meta['invested_money'] += tr.quantity * tr.price if tr.type == 4 else 0
            meta['received_dividends'] += tr.quantity * tr.price if tr.type == 5 else 0
            meta['transaction_costs'] += tr.cost

            return meta

        transactions = []
        meta = None

        if calc_meta:
            meta = {
                'invested_money': 0.0,
                'received_dividends': 0.0,
                'transaction_costs': 0.0,
            }

        for portfolio in self.portfolios.all():
            for transaction in portfolio.transactions.all():
                transactions.append(transaction)

                if calc_meta:
                    meta = calc_meta(meta, transaction)

        transactions.sort(key=lambda t: getattr(t, sort_by), reverse=sort_reverse)

        if calc_meta:
            return transactions, meta

        return transactions

    def calc_transaction_cost(self):
        return self.get_all_transactions(calc_meta=True)[1]['transaction_costs']

    def calc_invested_money(self):
        return self.get_all_transactions(calc_meta=True)[1]['invested_money']

    def get_monthly_transaction_data(self):
        transactions, meta = self.get_all_transactions(calc_meta=True)

        transactions.sort(key=lambda t: t.timestamp)  # todo sort by parameter

        data = {}
        meta = ['title', 'suffix', 'sort']

        for transaction in transactions:
            timestamp = transaction.timestamp
            month = timestamp.strftime('%b %Y')
            title = transaction.type_str.title
            suffix = transaction.type_str.suffix
            sort = transaction.type_str.sort
            type_str = title.replace(' ', '_').lower()

            value = transaction.price * transaction.quantity

            if type_str not in data:
                data[type_str] = {'title': title, 'suffix': suffix, 'sort': sort}

            if month not in data[type_str]:
                data[type_str][month] = {'total': []}
                data[type_str][month]['total'].append(value)
            else:
                data[type_str][month]['total'].append(value)

            if transaction.type == 1 or transaction.type == 3:
                type_str = 'bought_total'
                if type_str not in data:
                    data[type_str] = {'title': 'Bought (Total)', 'suffix': suffix, 'sort': 6}

                if month not in data[type_str]:
                    data[type_str][month] = {'total': []}
                    data[type_str][month]['total'].append(value)
                else:
                    data[type_str][month]['total'].append(value)

        for tr_type in data:
            data_absolute = [{'total': sum(data[tr_type][key]['total']), 'cnt': len(data[tr_type][key]['total'])} for
                             key in data[tr_type] if key not in meta]

            sum_data_absolute = sum([key['total'] for key in data_absolute])
            len_data_absolute = sum([key['cnt'] for key in data_absolute])

            print(data[type_str].keys())
            data[tr_type] = {
                'title': data[tr_type]['title'],
                'sort': data[tr_type]['sort'],
                'suffix': data[tr_type]['suffix'],
                'data_absolute': [key['total'] for key in data_absolute],
                'labels': [key for key in data[tr_type] if key not in meta],
                # 'average': round(sum_data_absolute / len_data_absolute, 2),
                'average': round(sum_data_absolute / 12, 2),
                'sum': round(sum_data_absolute, 2),
                'actions': len_data_absolute,
                'actions_month': round(len_data_absolute / 12, 2),
            }

        return {'keys': sorted(data, key=lambda x: data[x]['sort']), 'data': data}

    def get_asset_distribution(self):
        portfolios = self.portfolios.all()
        data = {}
        for portfolio in portfolios:
            pf_value = portfolio.value
            pf_type = portfolio.type_str.type

            if pf_type not in data:
                data[pf_type] = {'total': portfolio.value,
                                 'relative': pf_value / self.networth * 100}
            else:
                data[pf_type]['total'] += pf_value
                data[pf_type]['relative'] = data[pf_type]['total'] / self.networth * 100

        data = dict(sorted(data.items(), key=lambda t: t[1]['total'], reverse=True))

        return {'data_relative': [data[key]['relative'] for key in data],
                'data_absolute': [data[key]['total'] for key in data],
                'labels': list(data.keys())}

    def calculate_milestones(self):
        """
        calculate a milestone:
            - calc monthly average value
            - calc steps
        :return:
        """

        def calc_unit_per_day(starting_date, value):
            days_since_first_transaction = (datetime.now() - starting_date).days

            unit_per_day = value / days_since_first_transaction

            return unit_per_day if unit_per_day != 0 else 0.1

        def calc_steps(value):
            val = int(value)
            val_str = str(val)

            zeros = 10 ** (len(val_str) - 1)
            first_digit = int(val_str[0]) * zeros
            first_digit = 1 if first_digit == 0 else first_digit  # if first digit is zero, make it 1

            _steps = [x * zeros for x in [1.5, 2.5, 3.5, 5.0, 7.5, 10, 15, 35, 70]]

            steps = []

            for i, x in enumerate(_steps):
                x = first_digit * (x / first_digit)

                steps.append(first_digit + x)

            return steps

        def calc_expected_days_for_step(steps, value, profit_per_day):
            milestones = {}
            for step in steps:
                missing_value = step - value

                days = missing_value / profit_per_day
                days = datetime.now() + timedelta(days=days)

                milestones[step] = days.strftime('%d.%m.%Y')

            return milestones

        def _calculate_milestones(transactions, title, value, label_suffix='€'):
            starting_data = transactions[0].timestamp

            profit_per_day = calc_unit_per_day(starting_data, value)
            print('profit_per_day: ', profit_per_day)
            steps = calc_steps(value)
            print('steps: ', steps)
            milestone = calc_expected_days_for_step(steps, value, profit_per_day)

            return {
                'title': title,
                'milestones': milestone,
                'label_suffix': label_suffix,
            }

        transactions, meta = self.get_all_transactions(sort_reverse=False)
        transactions = transactions[1:]

        networth = meta['invested_money'] + self.profit_total_abs + meta['received_dividends'] - meta[
            'transaction_costs']

        dividends = self.expected_dividend
        result = []

        result.append(_calculate_milestones(transactions, 'Networth', networth))
        result.append(_calculate_milestones(transactions, 'Dividends', dividends))
        return result


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
