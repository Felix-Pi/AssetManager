from flask import render_template
from flask_breadcrumbs import register_breadcrumb

from app import db, User, Portfolio, USER_ID, app
from app.routes.index import bp

@bp.route('/')
@register_breadcrumb(app, '.', 'Home')
def index():
    portfolios = db.session.query(Portfolio).filter_by(user_id=USER_ID).all()
    user = db.session.query(User).filter_by(id=USER_ID).first()

    templateData = {
        'user': user,
        'portfolios': portfolios,
    }

    return render_template('index/index.html', **templateData, title=('Home'))
