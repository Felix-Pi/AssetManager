import pandas as pd

from flask import jsonify, request

from app import db, User, datetime
from app.domain_logic.YahooHistoricalData import get_historical_data_for_portfolio
from app.domain_logic.utils import get_csv_data
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

    file, creation_time, refresh = get_csv_data(domain, id, period, interval)
    if file is not None:
        if refresh is False:
            return pd.read_csv(file, index_col=0).to_json()

    get_historical_data_for_portfolio(id=id, period=period, interval=interval, domain=domain)
    return pd.read_csv(file, index_col=0).to_json()
