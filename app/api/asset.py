from flask import request, make_response, jsonify

from app import Asset, db
from app.api import *
from app.domain_logic.YahooHistoricalData import get_historical_data


def return_error(code, description):
    return make_response(jsonify(description), code)


@bp.route('/asset/<string:symbol>/historical_data', methods=['GET'])
def get_historical_data_(symbol):
    data = get_historical_data(symbol, request.args.get('days'),
                               request.args.get('period'))
    return jsonify(data)


@bp.route('/asset/<string:symbol>/recommendations', methods=['GET'])
def get_recommendations(symbol):
    asset = db.session.query(Asset).filter_by(symbol=symbol).first()

    data = asset.parse_recommendation_trend()
    if data is None:
        return return_error(404, 'no recommendations found')

    return jsonify(data)
