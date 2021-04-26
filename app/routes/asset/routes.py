from flask import render_template

from app import db, Asset
from app.routes.asset import bp


@bp.route('/<string:symbol>/')
def asset_index(symbol):
    asset = db.session.query(Asset).filter_by(symbol=symbol).first()

    templateData = {
        'asset': asset,
    }


    return render_template('assets/base.html', **templateData, title=('Home'))
