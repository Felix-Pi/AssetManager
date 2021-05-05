from app import db, Asset, Portfolio, User, app, Asset_types, datetime, json
from app.domain_logic.YahooApi import YahooApi
import yfinance as yf


def update_all_assets():
    assets = db.session.query(Asset).all()
    amount = len(assets)

    for i in range(amount):
        app.logger.info('[{}/{}] Updating symbol \'{}\''.format(i, amount, assets[i].symbol))
        update_asset(assets[i].symbol, debug=False)

    update_all_portfolio_positions()

def update_asset(symbol, debug=True):
    if debug:
        app.logger.info('Updating symbol \'{}\''.format(symbol))

    ticker = yf.Ticker(symbol)
    asset = db.session.query(Asset).filter_by(symbol=symbol).first()
    asset_data = ticker.info

    type = db.session.query(Asset_types).filter_by(type=asset_data['quoteType']).first()

    info = {
        'short_name': 'shortName',
        'long_name': 'longName',
        'type': type.id,
        'price_open': 'regularMarketOpen',
        'price': 'regularMarketPrice',
        'dividend': 'trailingAnnualDividendYield',
        'sector': 'sector',
        'industry': 'industry',
        'country': 'country',
        'currency': 'currency',
    }

    for key, value in info.items():
        if value in asset_data:
            setattr(asset, key, asset_data[value])

    if asset.dividend is None:
        asset.dividend = 0

    if asset.sector is None:
        asset.sector = 'other'

    if asset.country is None:
        asset.country = 'other'

    if asset.industry is None:
        asset.industry = 'other'

    db.session.commit()

    return asset


def add_symbol(symbol, type):
    fetch_existing = db.session.query(Asset).filter_by(symbol=symbol).first()

    if fetch_existing is not None:
        return fetch_existing

    asset = Asset(symbol=symbol, type=type)

    db.session.add(asset)
    db.session.commit()

    update_asset(asset.symbol)

    return asset


### Portfolio Stuff

def get_portfolio(id):
    return db.session.query(Portfolio).filter_by(id=id).first()


def update_all_portfolio_positions():
    portfolios = db.session.query(Portfolio).all()

    app.logger.info('Updating positions for all Portfolios ({}) '.format(len(portfolios)))
    for pf in portfolios:
        pf.update_portfolio_positions()


def add_transaction(pf_id, symbol, timestamp, transcation_type, price, quantity):
    portfolio = get_portfolio(pf_id)

    if symbol is not None:  # for transcation_type = 4
        fetch_existing = db.session.query(Asset).filter_by(symbol=symbol).first()

        if fetch_existing is None:
            symbol_type = YahooApi().get_symbol_type(symbol)

            asset_type = db.session.query(Asset_types).filter(Asset_types.type == symbol_type).first()

            add_symbol(symbol, asset_type.id)

    timestamp = datetime.strptime(timestamp, '%d.%m.%y')
    portfolio.add_transaction(symbol, transcation_type, timestamp, price, quantity)


### USER

def get_user(id):
    return db.session.query(User).filter_by(id=id).first()
