from assets import *
from portfolio import *



if __name__ == '__main__':
    database = r"data/database.db"

    conn = create_connection(database)
    with conn:
        update_assets(conn)
        update_portfolio_data(conn)

        update_portfolios(conn)


