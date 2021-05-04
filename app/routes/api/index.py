import os
import time
from datetime import timedelta

import pandas as pd

from flask import jsonify, request

from app import db, User, datetime
from app.domain_logic.YahooHistoricalData import get_historical_data_for_portfolio
from app.routes.api import *


@bp.route('/index/<int:user_id>/asset_distribution', methods=['GET'])
def get_index_asset_distribution(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()

    return jsonify(user.get_asset_distribution())


@bp.route('/index/<int:user_id>/monthly_transactions', methods=['GET'])
def get_monthly_transaction_page(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()

    return jsonify(user.get_monthly_transactions())


@bp.route('/index/<int:id>/historical_data', methods=['GET'])
def index_get_historical_data(id):
    period = request.args.get('period')
    interval = request.args.get('interval')

    domain = 'index'
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
