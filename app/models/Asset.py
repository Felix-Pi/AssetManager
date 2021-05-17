import json
import re
from datetime import datetime

from dateutil.relativedelta import relativedelta

from app import db


class Asset(db.Model):
    symbol = db.Column(db.String(64), primary_key=True, unique=True)
    alternative_symbol = db.Column(db.String(64))

    name = db.Column(db.String(64))
    short_name = db.Column(db.String(64))
    long_name = db.Column(db.String(64))

    type = db.Column(db.Integer, db.ForeignKey('asset_types.id'))
    type_str = db.relationship("Asset_types")

    price = db.Column(db.Float)
    price_open = db.Column(db.Float)
    dividend = db.Column(db.Float)

    sector = db.Column(db.String(64))
    industry = db.Column(db.String(64))

    country = db.Column(db.String(64))

    currency = db.Column(db.String(64))

    def get_name(self):
        def filter_asset_name(name):
            blacklist = [',', 'Inc.', 'Inc', 'S.A.', 'SE', '& Co. KGaA', ' AG', 'N.V.', 'ltd.', 'Ltd.', 'ltd',
                         'Limited', 'plc',
                         'Corp.', 'Holdings', 'Holding', 'Corporation', 'Aktiengesellschaft', '.com', '.dl-0001',
                         'UCITS', 'ETF', 'USD', '(Dist)', '(Acc)', 'Eur', 'iShares']

            for substr in blacklist:
                name = name.replace(substr.upper(), '')
                name = name.replace(substr, '')

            name = name.replace('amp;', '')

            return name

        name = self.long_name

        if name is not None:
            return filter_asset_name(name)

        if name is None:
            name = self.short_name
            name = filter_asset_name(name)
            name = ' '.join([word.capitalize() for word in name.lower().split(' ')])
            return name

        return self.symbol

    def to_dict(self):
        data = {
            'name': self.get_name(),
            'symbol': self.symbol,
            'alternative_symbol': self.alternative_symbol,
            'short_name': self.short_name,
            'long_name': self.long_name,
            'type': self.type,
            'price_open': self.price_open,
            'price': self.price,
            'dividend': self.dividend,
            'sector': self.sector,
            'industry': self.industry,
            'country': self.country,
        }

        return data

    def __repr__(self):
        return '<Asset {}>'.format(self.to_dict())


class Asset_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))
