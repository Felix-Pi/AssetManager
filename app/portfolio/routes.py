from flask import render_template, request

from app import db, Portfolio, USER_ID
from app.portfolio import bp


@bp.route('/')
def portfolio():
    portfolio_id = request.args.get('id', type=int)

    portfolio = db.session.query(Portfolio).filter_by(id=portfolio_id, user_id=USER_ID).first()

    #update_portfolio_positions(portfolio)

    templateData = {
        'portfolio': portfolio,
        'assets': portfolio.positions,
    }



    return render_template('portfolio/portfolio_base.html', **templateData, title=('Home'))