from flask import render_template, request, url_for
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_required, current_user

from app import db, Portfolio, User
from app.routes.portfolio import bp


def view_user_dlc(*args, **kwargs):
    portfolio_id = request.view_args['portfolio_id']
    portfolio = db.session.query(Portfolio).filter(Portfolio.id == portfolio_id).first()

    return [{'text': portfolio.title, 'url': url_for('portfolio.portfolio', portfolio_id=portfolio_id)}]


@bp.route('/<int:portfolio_id>/')
@register_breadcrumb(bp, '.portfolio', '', dynamic_list_constructor=view_user_dlc)
@login_required
def portfolio(portfolio_id):
    USER_ID = current_user.get_id()
    portfolio = db.session.query(Portfolio).filter_by(id=portfolio_id, user_id=USER_ID).first()
    user = db.session.query(User).filter_by(id=USER_ID).first()


    templateData = {
        'user': portfolio,
        'portfolio': portfolio,
        'assets': portfolio.positions,
    }

    return render_template('portfolio/portfolio_base.html', **templateData, title=('Home'))
