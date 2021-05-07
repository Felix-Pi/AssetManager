from flask import render_template
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_required, current_user
from sqlalchemy import desc

from app import db, User, Portfolio, app, Transaction_types
from app.routes.index import bp


@bp.route('/')
@register_breadcrumb(app, '.', 'Home')
@login_required
def index():
    USER_ID = current_user.get_id()
    portfolios = db.session.query(Portfolio).filter_by(user_id=USER_ID).all()
    user = db.session.query(User).filter_by(id=USER_ID).first()

    templateData = {
        'user': user,
        'portfolios': portfolios,
        'transaction_types': db.session.query(Transaction_types).order_by(Transaction_types.sort).all(),
    }

    return render_template('index/index.html', **templateData, title=('Home'))
