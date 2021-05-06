import os
import time
from datetime import timedelta

import pandas as pd

from flask import jsonify, request

from app import Portfolio, db, datetime
from app.domain_logic.YahooHistoricalData import get_historical_data_for_portfolio, get_historical_data
from app.domain_logic.utils import get_csv_data
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

    file, creation_time, refresh = get_csv_data(domain, id, period, interval)

    print(file, creation_time, refresh)
    if file is not None:
        if refresh is False:
            return pd.read_csv(file, index_col=0).to_json()

    return get_historical_data_for_portfolio(id=id, period=period, interval=interval, domain=domain)
    #return pd.read_csv(file, index_col=0).to_json()


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
