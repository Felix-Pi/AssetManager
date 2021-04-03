import time

from flask import Flask, render_template, request, url_for, jsonify, redirect, g
from assets import *
from portfolio import *
from db import *
from stock import *
from newsfeed import *
from utils import *

app = Flask(__name__, template_folder='www/templates/', static_folder='www/assets/')

USER_ID = 1
UPDATE_ALWAYS = True

database = r"data/database.db"


def update_data():
    conn = create_connection(database)
    update_data(conn)


def update_data(conn):
    with conn:
        update_assets(conn)
        update_portfolio_data(conn)

        update_portfolios(conn)


@app.route('/')
def index():
    conn = create_connection(database)
    with conn:
        portfolios = select_portfolios_from_user(conn, USER_ID)
        all_assets = select_all_assets(conn)
        keys = select_api_keys(conn)
        if UPDATE_ALWAYS:
            update_data(conn)

    all_portfolios = {'value': calc_all_portfolios_value(portfolios),
                      'profit_total_absolute': (calc_portfolio_profit(portfolios))[0],
                      'profit_total_relative': (calc_portfolio_profit(portfolios))[1],
                      'profit_today_absolute': (calc_portfolio_profit(portfolios))[2],
                      'profit_today_relative': (calc_portfolio_profit(portfolios))[3],
                      'dividend': calc_portfolio_dividend(portfolios)}

    # url_for('portfolio')
    templateData = {
        'pagetitle': 'Home',
        'portfolios': portfolios,
        'all_portfolios': all_portfolios,
        'news': get_news_for_ticker([asset['symbol'] for asset in all_assets], keys['news'])
    }

    return render_template('index.html', **templateData)


@app.route('/portfolio/')
def portfolio():
    portfolio_id = request.args.get('id', type=int)

    conn = create_connection(database)
    with conn:
        portfolio = select_portfolio(conn, portfolio_id)
        portfolio_value = portfolio[0]['portfolio_value']
        user_portfolios = select_portfolios_from_user(conn, USER_ID)
        assets = select_all_assets_from_portfolio(conn, portfolio_id)
        all_sectors = calc_sector_percentage(assets, portfolio_value, select_all_sectors(conn))
        if UPDATE_ALWAYS:
            update_data(conn)

    # portfolio percentage
    for data in assets:
        data['portfolio_percentage'] = calc_portfolio_percentage(portfolio_value, data['asset_value'])

    templateData = {
        'pagetitle': 'Portfolio',
        'portfolio_id': portfolio_id,  # the current portfolio
        'portfolio': portfolio,  # the current portfolio
        'user_portfolios': user_portfolios,  # all portfolios owned by that user
        'user_portfolios_with_same_type': [p for p in user_portfolios if
                                           p['portfolio_type'] == portfolio[0]['portfolio_type']],
        # all portfolios owned by that user
        'assets': assets,  # assets in this portfolio
        'all_sectors': all_sectors,  # assets in this portfolio
        'news': get_news_for_ticker([asset['symbol'] for asset in assets if 'symbol' in asset])
    }
    return render_template('portfolio/portfolio.html', **templateData)


@app.route('/stock/')
def stock():
    portfolio_id = request.args.get('portfolio', type=int)
    stock_id = request.args.get('stock', type=int)
    conn = create_connection(database)

    with conn:
        stock = select_single_asset_from_portfolio(conn, portfolio_id, stock_id)[0]
        symbol = stock['symbol']
        keys = select_api_keys(conn)
        if UPDATE_ALWAYS:
            update_data(conn)

    templateData = {
        'pagetitle': 'Portfolio',
        'stock': stock,
        'general_info': get_asset_profile(symbol),
        'news': get_news_for_ticker(symbol, keys['news'])
    }

    return render_template('assets/stock.html', **templateData)


@app.route('/api/refresh/')
def refresh_data():
    update_data()
    return redirect(url_for(request.args.get('redirect').replace('\'', '')))


@app.route('/api/select_single_asset_from_portfolio/', methods=['POST'])
def api_select_single_asset_from_portfolio():
    if request.method == 'POST':
        conn = create_connection(database)
        with conn:
            return jsonify(
                select_single_asset_from_portfolio(conn, request.form['portfolio_id'], request.form['asset_id']))


@app.route('/api/stock/<endpoint>/', methods=['GET', 'POST'])
def api_stock_endpoint(endpoint):
    if request.method == 'GET':
        if 'yahoo_search' == endpoint:
            return yahoo_search_request(request.args.get('input'), 'US', 'en-US')
        if 'get_recommendation_trend' == endpoint:
            return get_recommendation_trend(request.args.get('symbol'))
        if 'historical_data' == endpoint:
            print(request.args)
            return get_historical_data(request.args.get('symbols'), request.args.get('days'),
                                       request.args.get('period'))
        if 'endpoint' == endpoint:
            print(endpoint)

    if request.method == 'POST':
        if 'endpoint' == endpoint:
            print(endpoint)

    return endpoint


@app.route('/api/portfolio/<endpoint>/', methods=['GET', 'POST'])
def api_portfolio_endpoint(endpoint):
    if request.method == 'GET':
        if 'get_stock_distribution' == endpoint:
            print(endpoint)
        if 'get_country_data' == endpoint:
            conn = create_connection(database)
            with conn:
                data = db_get_country_data_for_portfolio(conn, request.args.get('portfolio_id'))
                print(data)
                return json.dumps({'data': [data['amount'] for data in data],
                                   'labels': [data['country'] for data in data]})
        if 'get_country_dataold' == endpoint:
            conn = create_connection(database)
            with conn:
                return json.dumps(db_get_country_data_for_portfolio(conn, request.args.get('portfolio_id')))
        if 'get_stock_distribution' == endpoint:
            conn = create_connection(database)
            with conn:
                portfolio_id = request.args.get('portfolio_id')
                portfolio = select_portfolio(conn, portfolio_id)
                portfolio_value = portfolio[0]['portfolio_value']
                assets = select_all_assets_from_portfolio(conn, portfolio_id)
                all_sectors = calc_sector_percentage(assets, portfolio_value, select_all_sectors(conn))

                return json.dumps({'data': [asset['asset_value'] for asset in assets],
                                   'labels': [asset['title'] for asset in assets]})
        if 'get_sector_distribution' == endpoint:
            conn = create_connection(database)
            with conn:
                portfolio_id = request.args.get('portfolio_id')
                portfolio = select_portfolio(conn, portfolio_id)
                portfolio_value = portfolio[0]['portfolio_value']
                assets = select_all_assets_from_portfolio(conn, portfolio_id)
                all_sectors = calc_sector_percentage(assets, portfolio_value, select_all_sectors(conn))

                return json.dumps({'data': [asset['percentage'] for asset in all_sectors],
                                   'labels': [asset['title'] for asset in all_sectors]})
        if 'endpoint' == endpoint:
            print(endpoint)
    if request.method == 'POST':
        if 'update_stock' == endpoint:
            conn = create_connection(database)
            with conn:
                api_portfolio_update_stock(conn, request.form)
        if 'add_stock' == endpoint:
            conn = create_connection(database)
            with conn:
                if check_if_asset_symbol_exists(request.form['symbol']):
                    api_portfolio_insert_stock(conn, request.form)

            update_data()
            return 'True'
        if 'endpoint' == endpoint:
            print(endpoint)
    return endpoint


@app.route('/api/index/<endpoint>/', methods=['GET', 'POST'])
def api_index_endpoint(endpoint):
    if request.method == 'GET':
        if 'get_asset_distribution' == endpoint:
            conn = create_connection(database)
            with conn:
                doughnut_asset_allocation = select_assets_from_portfolio_grouped_by_sector(conn, USER_ID)
                return json.dumps({
                    'data': [asset['val'] for asset in doughnut_asset_allocation],
                    'labels': [asset['title'] for asset in doughnut_asset_allocation],
                })
        if 'endpoint' == endpoint:
            print(endpoint)
    return endpoint


if __name__ == '__main__':
    app.run(debug=True, port=81, host='0.0.0.0')
