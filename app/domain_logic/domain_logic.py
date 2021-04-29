from app import db, Asset, Stock_data, Etf_data, Crypto_data, Portfolio, User, app, Currency_data, Asset_types, datetime
from app.domain_logic.YahooApi import YahooApi
from app.domain_logic.asset_templates import stock_api_template, etf_api_template, crypto_api_template, price_template, \
    currency_template


### Asset Stuff


def update_all_assets_full():
    for asset in db.session.query(Asset).all():
        update_asset_full(asset)

    update_all_portfolio_positions()


def update_asset_full(asset):
    if asset.type == 1:
        template = stock_api_template
    if asset.type == 2:
        template = etf_api_template
    if asset.type == 3:
        template = crypto_api_template
    if asset.type == 4:
        template = currency_template

    symbol = asset.symbol

    # use alternative symbol on update
    # if asset.alternative_symbol is not None:
    #     symbol=asset.alternative_symbol

    dataset = YahooApi().build_data(symbol, template)
    if 'symbol' in dataset:
        dataset.pop('symbol')
    if 'modules' in dataset:
        dataset.pop('modules')

    update_asset_data(asset.symbol, dataset)


def update_asset_data(symbol, dataset):
    asset = db.session.query(Asset).filter_by(symbol=symbol).first()

    asset.price = dataset['price']
    asset.price_open = dataset['price_open']
    db.session.commit()

    if asset.type == 1:
        asset_data = db.session.query(Stock_data).filter_by(symbol=asset.symbol).first()

        asset_data_is_none = asset_data is None
        if asset_data_is_none:
            asset_data = Stock_data(**dataset, symbol=symbol)
    if asset.type == 2:
        asset_data = db.session.query(Etf_data).filter_by(symbol=asset.symbol).first()

        asset_data_is_none = asset_data is None
        if asset_data_is_none:
            asset_data = Etf_data(**dataset, symbol=symbol)
    if asset.type == 3:
        asset_data = db.session.query(Crypto_data).filter_by(symbol=asset.symbol).first()

        asset_data_is_none = asset_data is None
        if asset_data_is_none:
            asset_data = Crypto_data(**dataset, symbol=symbol)
    if asset.type == 4:
        asset_data = db.session.query(Currency_data).filter_by(symbol=asset.symbol).first()

        asset_data_is_none = asset_data is None
        if asset_data_is_none:
            asset_data = Currency_data(**dataset, symbol=symbol)

    if asset_data_is_none:
        db.session.add(asset_data)
        db.session.commit()
    else:
        for key in dataset:
            setattr(asset_data, key, dataset[key])

    if asset.asset_data_id is None:
        setattr(asset, 'asset_data_id', asset_data.id)
        db.session.commit()

    db.session.commit()

    return asset


def update_all_assets_price():
    assets = db.session.query(Asset).all()
    app.logger.info('Updating Price for all assets ({}) '.format(len(assets)))

    for asset in assets:
        template = price_template

        if asset.type == 4:
            template = currency_template

        dataset = YahooApi().build_data(asset.symbol, template)
        dataset.pop('modules')

    update_all_portfolio_positions()


def add_symbol(symbol, typee):
    def search_alternative_symbol(symbol):
        alt_exchanges = ['NQY', 'NMS', 'FRA']
        api = YahooApi()
        res, title = api.search_alternative_symbols(symbol)

        if res is not None:
            for alt_symbol in res:
                if alt_symbol['symbol'] != symbol:
                    return alt_symbol['symbol'], title

        return None, title
        # search for NASDAQ (NMS)
        # alternative_symbol=None
        # for alt_symbol in res:
        #     print(symbol, alt_symbol['exchange'], alt_symbol['symbol'])
        #     if alt_symbol['exchange'] in alt_exchanges:
        #         alternative_symbol=alt_symbol['symbol']
        #         # return alternative_symbol
        #
        # if alternative_symbol != symbol:
        #     return alternative_symbol, title
        #
        # return None, title

    fetch_existing = db.session.query(Asset).filter_by(symbol=symbol).first()

    if fetch_existing is not None:
        return fetch_existing

    alternative_symbol, title = search_alternative_symbol(symbol)

    if title is not None:
        title = title.lower()
        title = title.capitalize()

    if title is None or len(title) < 1:
        title = symbol

    app.logger.info('Alternative symbol for {}: \'{}\'->\'{}\''.format(title, symbol, alternative_symbol))
    asset = Asset(symbol=symbol, title=title, type=typee, alternative_symbol=alternative_symbol)

    db.session.add(asset)
    db.session.commit()

    update_asset_full(asset)

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

# 1 - Buy
# 2 - Sell
# 3 - monthly
# 4 - Money Transfer
# 5 - Dividend
