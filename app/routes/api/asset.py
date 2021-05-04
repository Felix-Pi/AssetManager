from flask import request, make_response, jsonify

from app import Asset, db
from app.domain_logic.utils import return_error
from app.routes.api import *
from app.domain_logic.YahooHistoricalData import get_historical_data, get_historical_data_for_portfolio


@bp.route('/asset/<string:symbol>/historical_data', methods=['GET'])
def get_historical_data_(symbol):
    period = request.args.get('period')
    interval = request.args.get('interval')


    data = get_historical_data(symbol=symbol,
                               period=period,
                               interval=interval)
    return jsonify(data)


@bp.route('/asset/<string:symbol>/recommendations', methods=['GET'])
def get_recommendations(symbol):
    asset = db.session.query(Asset).filter_by(symbol=symbol).first()

    data = asset.parse_recommendation_trend()
    if data is None:
        return return_error(416, 'no recommendations found')

    return jsonify(data)
