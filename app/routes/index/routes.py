from flask import render_template
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_required, current_user

from app import db, User, Portfolio, app
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
    }

    return render_template('index/index.html', **templateData, title=('Home'))
