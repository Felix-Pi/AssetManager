from flask import jsonify

from app import update_all_portfolio_positions, update_all_assets, update_all_prices
from app.routes.api import bp

@bp.route('/update_all_prices', methods=['GET'])
def api_update_prices():
    result = update_all_prices()


    return jsonify(True)

@bp.route('/update_data_full', methods=['GET'])
def api_update_data_full():
    update_all_assets()

    return jsonify(True)

