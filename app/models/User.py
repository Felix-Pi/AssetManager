from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prename = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    portfolios = db.relationship("Portfolio", backref='user', lazy='dynamic')

    @staticmethod
    def get_user(id):
        return db.session.query(User).filter_by(id=id).first()

    def get_name(self):
        return self.prename + ' ' + self.surname

    def calc_networth(self):
        return round(sum([pf.calc_portfolio_value() for pf in self.portfolios.all()]), 2)

    def calc_profit(self):
        return {
            'profit_today_absolute': 0,
            'profit_today_relative': 0,
            'profit_total_absolute': 0,
            'profit_total_relative': 0,
        }

    def calc_profit(self):
        networth = self.calc_networth()

        profit_total_absolute = round(
            sum([pf.calc_portfolio_profit()['total_absolute'] for pf in self.portfolios.all()]), 2)
        profit_today_absolute = round(
            sum([pf.calc_portfolio_profit()['today_absolute'] for pf in self.portfolios.all()]), 2)

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

    def get_asset_distribution(self):

        portfolios = self.portfolios.all()
        data = {}
        for portfolio in portfolios:
            networth = self.calc_networth()
            pf_value = portfolio.calc_portfolio_value()
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

    def __repr__(self):
        return '<User {}>'.format(self.get_name())
