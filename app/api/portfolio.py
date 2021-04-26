from flask import jsonify

from app import Portfolio, db
from app.api import *

def get_portfolio(id):
    return db.session.query(Portfolio).filter_by(id=id).first()

@bp.route('/portfolio/<int:id>/stock_distribution', methods=['GET'])
def get_stock_distribution(id):
    pf = get_portfolio(id)
    return jsonify(pf.calc_stock_distribution())


@bp.route('/portfolio/<int:id>/sector_distribution', methods=['GET'])
def get_sector_distribution(id):
    pf = get_portfolio(id)
    return jsonify(pf.calc_sector_distribution())


@bp.route('/portfolio/<int:id>/country_distribution', methods=['GET'])
def get_country_distribution(id):
    pf = get_portfolio(id)
    return jsonify(pf.calc_country_distribution())


@bp.route('/portfolio/<int:portfolio_id>/asset/<int:asset_id>', methods=['GET'])
def get_asset_from_portfolio(portfolio_id, asset_id):
    pass


@bp.route('/portfolio/<int:id>/followers', methods=['GET'])
def get_followers(id):
    pass


@bp.route('/portfolio/<int:id>/followed', methods=['GET'])
def get_followed(id):
    pass


@bp.route('/portfolio', methods=['POST'])
def create_user():
    pass


@bp.route('/portfolio/<int:id>', methods=['PUT'])
def update_user(id):
    pass
