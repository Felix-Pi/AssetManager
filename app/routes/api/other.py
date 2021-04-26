from flask import jsonify

from app import Asset, Portfolio
from app.routes.api import bp


@bp.route('/update_all', methods=['GET'])
def update_everything():
    update_all_assets_price()
    Portfolio.update_all_portfolio_positions()

    return jsonify(True)
