from flask import jsonify

from app import update_all_portfolio_positions, update_all_assets
from app.routes.api import bp

@bp.route('/update_data_full', methods=['GET'])
def update_data_full():
    update_all_assets()

    return jsonify(True)

