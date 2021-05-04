import os
import time
from datetime import timedelta

import pandas as pd

from flask import jsonify, request

from app import Portfolio, db, datetime
from app.domain_logic.YahooHistoricalData import get_historical_data_for_portfolio
from app.routes.api import *


def get_portfolio(id):
    return db.session.query(Portfolio).filter_by(id=id).first()


@bp.route('/portfolio/<int:id>/stock_distribution', methods=['GET'])
def get_stock_distribution(id):
    pf = get_portfolio(id)
    return jsonify(pf.calc_stock_distribution())


@bp.route('/portfolio/<int:id>/historical_data', methods=['GET'])
def pf_get_historical_data(id):
    period = request.args.get('period')
    interval = request.args.get('interval')

    domain = 'portfolio'
    file = 'data/csv/{}/{}_{}_{}_{}.csv'.format(domain, domain, id, period, interval)

    if os.path.isfile(file):
        stat = os.stat(file)
        creation_time = datetime.fromtimestamp(stat.st_birthtime)

        if '1d' == period or '2d' == period:
            condition_time = datetime.now() - timedelta(hours=1)
        else:
            condition_time = datetime.now() - timedelta(days=1)

        if creation_time > condition_time:
            return pd.read_csv(file, index_col=0).to_json()
        else:
            get_historical_data_for_portfolio(id=id,
                                              period=period,
                                              interval=interval,
                                              domain=domain)
            return pd.read_csv(file, index_col=0).to_json()

    else:
        data = get_historical_data_for_portfolio(id=id,
                                                 period=period,
                                                 interval=interval,
                                                 domain=domain)

        return jsonify(data)


@bp.route('/portfolio/<int:id>/sector_distribution', methods=['GET'])
def get_sector_distribution(id):
    pf = get_portfolio(id)
    return jsonify(pf.calc_sector_distribution())


@bp.route('/portfolio/<int:id>/industry_distribution', methods=['GET'])
def get_industry_distribution(id):
    pf = get_portfolio(id)
    return jsonify(pf.calc_industry_distribution())


@bp.route('/portfolio/<int:id>/country_distribution', methods=['GET'])
def get_country_distribution(id):
    pf = get_portfolio(id)
    return jsonify(pf.calc_country_distribution())
