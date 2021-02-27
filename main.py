from assets import *
from portfolio import *


def save_result(file, data):
    f = open(file, 'w')
    f.write(json.dumps(data))
    f.close()


if __name__ == '__main__':
    database = r"data/database.db"

    conn = create_connection(database)
    with conn:
        assets = select_all_symbols(conn)
        portfolios = select_all_portfolios(conn)

    assets = prepare_assets(assets)
    save_result('data/json/assets.json', assets)

    portfolios, all_portfolios = prepare_portfolios(portfolios, assets)

    save_result('data/json/portfolios.json', portfolios)
    save_result('data/json/all_portfolios.json', all_portfolios)
