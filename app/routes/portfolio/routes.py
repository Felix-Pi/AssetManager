from flask import render_template, request, url_for
from flask_breadcrumbs import register_breadcrumb

from app import db, Portfolio, USER_ID
from app.routes.portfolio import bp


def view_user_dlc(*args, **kwargs):
    portfolio_id = request.view_args['portfolio_id']
    portfolio = db.session.query(Portfolio).filter(Portfolio.id == portfolio_id).first()

    return [{'text': portfolio.title, 'url': url_for('portfolio.portfolio', portfolio_id=portfolio_id)}]


@bp.route('/<int:portfolio_id>/')
@register_breadcrumb(bp, '.portfolio', '', dynamic_list_constructor=view_user_dlc)
def portfolio(portfolio_id):
    portfolio = db.session.query(Portfolio).filter_by(id=portfolio_id, user_id=USER_ID).first()

    # update_portfolio_positions(portfolio)

    templateData = {
        'portfolio': portfolio,
        'assets': portfolio.positions,
    }

    return render_template('portfolio/portfolio_base.html', **templateData, title=('Home'))
