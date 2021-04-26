from flask import jsonify

from app import db, User
from app.api import *


@bp.route('/index/<int:user_id>/asset_distribution', methods=['GET'])
def get_index_asset_distribution(user_id):
    user = db.session.query(User).filter_by(id=user_id).first()

    return jsonify(user.get_asset_distribution())