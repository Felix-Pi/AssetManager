from flask import Flask, render_template, request, url_for, jsonify
from assets import *
from portfolio import *
from mysql import *
from stock import *

app = Flask(__name__, template_folder='www/templates/', static_folder='www/assets/')

USER_ID = 1
database = r"data/database.db"


@app.route('/')
def index():
    conn = create_connection(database)
    with conn:
        portfolios = select_portfolios_from_user(conn, USER_ID)

        doughnut_asset_allocation = select_assets_from_portfolio_grouped_by_sector(conn, USER_ID)
    all_portfolios = {'value': calc_all_portfolios_value(portfolios),
                      'profit_total_absolute': (calc_portfolio_profit(portfolios))[0],
                      'profit_today_absolute': (calc_portfolio_profit(portfolios))[1],
                      'dividend': calc_portfolio_dividend(portfolios)}

    # url_for('portfolio')
    templateData = {
        'pagetitle': 'Home',
        'portfolios': portfolios,
        'all_portfolios': all_portfolios,
        'doughnut_asset_allocation_data': [asset['val'] for asset in doughnut_asset_allocation],
        'doughnut_asset_allocation_label': [asset['title'] for asset in doughnut_asset_allocation],
    }
    return render_template('index.html', **templateData)


@app.route('/portfolio/')
def portfolio():
    portfolio_id = request.args.get('id', type=int)

    conn = create_connection(database)
    with conn:
        portfolio = select_portfolio(conn, portfolio_id)
        user_portfolios = select_portfolios_from_user(conn, USER_ID)
        assets = select_all_assets_from_portfolio(conn, portfolio_id)
        doughnut_sector = select_sectordata_from_portfolio_grouped_by_sector(conn, portfolio_id)
        all_sectors = select_all_sectors(conn)

    print('user_portfolios', user_portfolios)
    templateData = {
        'pagetitle': 'Portfolio',
        'portfolio_id': portfolio_id,  # the current portfolio
        'portfolio': portfolio,  # the current portfolio
        'user_portfolios': user_portfolios,  # all portfolios owned by that user
        'assets': assets,  # assets in this portfolio
        'all_sectors': all_sectors,  # assets in this portfolio
        'percentage_doughnut_data': [asset['asset_value'] for asset in assets],
        'percentage_doughnut_label': [asset['title'] for asset in assets],
        'doughnut_sector_data': [asset['val'] for asset in doughnut_sector],
        'doughnut_sector_label': [asset['title'] for asset in doughnut_sector],
    }
    return render_template('portfolio.html', **templateData)


@app.route('/stock/')
def stock():
    portfolio_id = request.args.get('portfolio', type=int)
    stock_id = request.args.get('stock', type=int)
    conn = create_connection(database)
    with conn:
        stock = select_single_asset_from_portfolio(conn, portfolio_id, stock_id)
        stock_price_linechart = get_historical_data()

    templateData = {
        'pagetitle': 'Portfolio',
        'stock_price_linechart': {'data': stock_price_linechart[0], 'label': stock_price_linechart[1]}

    }
    return render_template('assets/stock.html', **templateData)


@app.route('/api/refresh/')
def refresh_data():
    database = r"data/database.db"

    conn = create_connection(database)
    with conn:
        update_assets(conn)
        update_portfolio_data(conn)

        update_portfolios(conn)

    return 'updated'


@app.route('/api/select_single_asset_from_portfolio/', methods=['POST'])
def api_select_single_asset_from_portfolio():
    if request.method == 'POST':
        conn = create_connection(database)
        with conn:
            return jsonify(
                select_single_asset_from_portfolio(conn, request.form['portfolio_id'], request.form['asset_id']))


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
