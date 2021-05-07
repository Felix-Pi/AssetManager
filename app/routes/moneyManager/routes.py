from flask import render_template
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_required, current_user

from app import db, User, Portfolio, app
from app.routes.moneyManager import bp


@bp.route('/')
@register_breadcrumb(app, '.moneyManager', 'MoneyManager')
@login_required
def moneyManager():
    USER_ID = current_user.get_id()
    user = db.session.query(User).filter_by(id=USER_ID).first()

    templateData = {
        'user': user,
    }

    return render_template('moneyManager/base.html', **templateData, title=('MoneyManager'))
