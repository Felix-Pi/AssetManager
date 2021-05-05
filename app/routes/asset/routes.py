from flask import render_template, request, url_for
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_required, current_user

from app import db, Asset, Portfolio_positions, Portfolio, User
from app.routes.asset import bp

import yfinance as yf
import requests_cache


def view_user_dlc(*args, **kwargs):
    portfolio_id = request.view_args['portfolio_id']
    symbol = request.view_args['symbol']

    return [{'text': symbol, 'url': url_for('asset.asset_index', symbol=symbol, portfolio_id=portfolio_id)}]


@bp.route('/<int:portfolio_id>/<string:symbol>/')
@register_breadcrumb(bp, '.portfolio.asset_index', 'Asset', dynamic_list_constructor=view_user_dlc)
@login_required
def asset_index(portfolio_id, symbol):
    USER_ID = current_user.get_id()
    user = db.session.query(User).filter_by(id=USER_ID).first()

    asset = db.session.query(Asset).filter_by(symbol=symbol).first()
    position = db.session.query(Portfolio_positions).filter(Portfolio_positions.symbol == symbol,
                                                            Portfolio_positions.portfolio == portfolio_id).first()

    session = requests_cache.CachedSession('yfinance.cache')

    ticker = yf.Ticker(asset.symbol, session=session)

    templateData = {
        'user': user,
        'asset': asset,
        'position': position,
        'info': ticker.info,

        'dividends': ticker.dividends,
        'splits': ticker.splits,
        'financials': ticker.financials,

        'quarterly_financials': ticker.quarterly_financials,
        'major_holders': ticker.major_holders,
        'institutional_holders': ticker.institutional_holders,
        'balance_sheet': ticker.balance_sheet,
        'quarterly_balance_sheet': ticker.quarterly_balance_sheet,
        'cashflow': ticker.cashflow,
        'quarterly_cashflow': ticker.quarterly_cashflow,
        'earnings': ticker.earnings,
        'quarterly_earnings': ticker.quarterly_earnings,
        'sustainability': ticker.sustainability,
        'recommendations': ticker.recommendations,
        'calendar': ticker.calendar,
        'isin': ticker.isin,
    }

    for k, v in templateData['recommendations'].items():
        print(k, v)



    # print('dividends: ', templateData['dividends'])
    # print('splits: ', templateData['splits'])
    # print('financials: ', templateData['financials'])
    # print('quarterly_financials: ', templateData['quarterly_financials'])
    # print('major_holders: ', templateData['major_holders'])
    # print('institutional_holders: ', templateData['institutional_holders'])
    # print('balance_sheet: ', templateData['balance_sheet'])
    # print('quarterly_balance_sheet: ', templateData['quarterly_balance_sheet'])
    # print('cashflow: ', templateData['cashflow'])
    # print('quarterly_cashflow: ', templateData['quarterly_cashflow'])
    # print('earnings: ', templateData['earnings'])
    # print('quarterly_earnings: ', templateData['quarterly_earnings'])
    # print('sustainability: ', templateData['sustainability'])
    # print('recommendations: ', templateData['recommendations'])
    # print('calendar: ', templateData['calendar'])
    # print('isin: ', templateData['isin'])

    return render_template('assets/base.html', **templateData, title=('Home'))
