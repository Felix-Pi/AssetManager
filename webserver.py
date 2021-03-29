import time

from flask import Flask, render_template, request, url_for, jsonify, redirect
from assets import *
from portfolio import *
from db import *
from stock import *
from newsfeed import *

app = Flask(__name__, template_folder='www/templates/', static_folder='www/assets/')

USER_ID = 1
database = r"data/database.db"


def update_data():
    conn = create_connection(database)
    with conn:
        update_assets(conn)
        update_portfolio_data(conn)

        update_portfolios(conn)


@app.route('/')
def index():
    conn = create_connection(database)
    with conn:
        portfolios = select_portfolios_from_user(conn, USER_ID)

        doughnut_asset_allocation = select_assets_from_portfolio_grouped_by_sector(conn, USER_ID)
        all_assets = select_all_assets(conn)

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
        'doughnut_asset_allocation_data': [asset['val'] for asset in doughnut_asset_allocation],
        'doughnut_asset_allocation_label': [asset['title'] for asset in doughnut_asset_allocation],
        'news': get_news_for_ticker([asset['symbol'] for asset in all_assets])
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
        'percentage_doughnut_data': [asset['asset_value'] for asset in assets],
        'percentage_doughnut_label': [asset['title'] for asset in assets],
        'doughnut_sector_data': [asset['percentage'] for asset in all_sectors],
        'doughnut_sector_label': [asset['title'] for asset in all_sectors],
        'news': get_news_for_ticker([asset['symbol']  for asset in assets if 'symbol' in asset])
    }
    return render_template('portfolio/portfolio.html', **templateData)


@app.route('/stock/')
def stock():
    portfolio_id = request.args.get('portfolio', type=int)
    stock_id = request.args.get('stock', type=int)
    conn = create_connection(database)
    with conn:
        stock = select_single_asset_from_portfolio(conn, portfolio_id, stock_id)[0]

        stock_price_linechart = get_historical_data(stock['symbol'])

    templateData = {
        'pagetitle': 'Portfolio',
        'stock_price_linechart': {'data': stock_price_linechart[0], 'label': stock_price_linechart[1]},
        'news': get_news_for_ticker(stock['symbol'])
    }
    return render_template('assets/stock.html', **templateData)


@app.route('/api/refresh/')
def refresh_data():
    update_data()

    return redirect(url_for('index'))


@app.route('/api/select_single_asset_from_portfolio/', methods=['POST'])
def api_select_single_asset_from_portfolio():
    if request.method == 'POST':
        conn = create_connection(database)
        with conn:
            return jsonify(
                select_single_asset_from_portfolio(conn, request.form['portfolio_id'], request.form['asset_id']))


@app.route('/api/portfolio/add_stock/', methods=['POST'])
def api_portfolio_add_stock():
    if request.method == 'POST':
        conn = create_connection(database)
        with conn:
            if check_if_asset_symbol_exists(request.form['symbol']):
                api_portfolio_insert_stock(conn, request.form)

        update_data()

        # redirect(url_for('portfolio')) #todo portfolio id
        return "true"


@app.route('/api/portfolio/update_stock/', methods=['POST'])
def api_portfolio_edit_stock():
    if request.method == 'POST':
        conn = create_connection(database)
        with conn:
            api_portfolio_update_stock(conn, request.form)

        update_data()
        # redirect(url_for('portfolio') + '?id=' + po) #todo portfolio id

    return "true"

if __name__ == '__main__':
    app.run(debug=True, port=81, host='0.0.0.0')
