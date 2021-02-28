from flask import Flask, render_template, request
from assets import *
from portfolio import *
from mysql import *

app = Flask(__name__)

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

    print(portfolios)

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
        portfolio = select_portfolio(conn, portfolio_id)[0]
        assets = select_assets_from_portfolio(conn, portfolio_id)
        doughnut_sector = select_sectordata_from_portfolio_grouped_by_sector(conn, portfolio_id)


    print(doughnut_sector)
    templateData = {
        'pagetitle': 'Portfolio',
        'portfolio': portfolio,
        'assets': assets,
        'percentage_doughnut_data': [asset['asset_value'] for asset in assets],
        'percentage_doughnut_label': [asset['title'] for asset in assets],
        'doughnut_sector_data': [asset['val'] for asset in doughnut_sector],
        'doughnut_sector_label': [asset['title'] for asset in doughnut_sector],
    }
    return render_template('portfolio.html', **templateData)

    return json.dumps({'data': data, 'labels': [labels]})


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
