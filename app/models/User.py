from datetime import time, datetime
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

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

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

    def calc_networth(self):
        return round(sum([pf.calc_value() for pf in self.portfolios.all()]), 2)

    def calc_profit(self):  # todo remove profit_
        networth = self.calc_networth()

        profit_total_absolute = round(
            sum([pf.calc_profit()['total_absolute'] for pf in self.portfolios.all()]), 2)
        profit_today_absolute = round(
            sum([pf.calc_profit()['today_absolute'] for pf in self.portfolios.all()]), 2)

        profit_total_relative = profit_total_absolute / networth * 100
        profit_today_relative = profit_today_absolute / networth * 100

        data = {
            'profit_today_absolute': round(profit_today_absolute, 2),
            'profit_today_relative': round(profit_today_relative, 2),
            'profit_total_absolute': round(profit_total_absolute, 2),
            'profit_total_relative': round(profit_total_relative, 2),
        }
        return data

    def calc_dividend(self):
        return sum([pf.calc_dividend() for pf in self.portfolios.all()])

    def get_all_transactions(self):
        transactions = []
        for portfolio in self.portfolios.all():
            for transaction in portfolio.transactions.all():
                transactions.append(transaction)

        transactions.sort(key=lambda t: t.timestamp, reverse=True)

        return transactions

    def calc_transaction_cost(self):
        portfolios = self.portfolios.all()

        res = 0.0
        for portfolio in portfolios:
            for pos in portfolio.transactions.all():
                res += pos.cost

        return res

    def get_monthly_transaction_data(self):
        transactions = self.get_all_transactions()

        transactions.sort(key=lambda t: t.timestamp)

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
            networth = self.calc_networth()
            pf_value = portfolio.calc_value()
            pf_type = portfolio.type_str.type

            if pf_type not in data:
                data[pf_type] = {'total': portfolio.value,
                                 'relative': pf_value / networth * 100}
            else:
                data[pf_type]['total'] += pf_value
                data[pf_type]['relative'] = data[pf_type]['total'] / networth * 100

        data = dict(sorted(data.items(), key=lambda t: t[1]['total'], reverse=True))

        return {'data_relative': [data[key]['relative'] for key in data],
                'data_absolute': [data[key]['total'] for key in data],
                'labels': list(data.keys())}


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
