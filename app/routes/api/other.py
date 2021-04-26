from flask import jsonify

from app import update_all_assets_price, update_all_portfolio_positions, update_all_assets_full
from app.routes.api import bp


@bp.route('/update_data_price', methods=['GET'])
def update_data_price():
    update_all_assets_price()

    return jsonify(True)


@bp.route('/update_data_full', methods=['GET'])
def update_data_full():
    update_all_assets_full()

    return jsonify(True)
