import sqlite3
from sqlite3 import Error


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.row_factory = dict_factory
    except Error as e:
        print(e)

    return conn


def update_all_assets(conn, assets):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """

    for data in assets:
        dataset = (data['regularMarketPrice'],
                   data['regularMarketOpen'],
                   data['trailingAnnualDividendRate'],
                   data['trailingAnnualDividendYield'],
                   data['id'])


        sql = ''' UPDATE assets
                  SET regularMarketPrice          = ? ,
                      regularMarketOpen           = ? ,
                      trailingAnnualDividendRate  = ? ,
                      trailingAnnualDividendYield = ?
                  WHERE id = ?'''
        cur = conn.cursor()
        cur.execute(sql, dataset)
        conn.commit()


def select_all_symbols(conn):
    """
    Query tasks by priority
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()

    cur.execute('SELECT * FROM assets WHERE asset_type != 4')

    return cur.fetchall()


def select_all_portfolios(conn):
    """
    Query tasks by priority
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute('SELECT * FROM portfolios')

    return cur.fetchall()


def select_portfolios_data_for_prepare(conn):
    """
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    # cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))

    sql = 'SELECT pd.id, pd.quantity, pd.buyIn, pd.sector, a.* ' \
          'FROM portfolio_data pd ' \
          'JOIN assets a on a.id = pd.asset WHERE a.asset_type != 4'  # dont select assets with type cash

    cur.execute(sql)

    return cur.fetchall()


def select_portfolio_data(conn, portfolio_id):
    cur = conn.cursor()
    sql = "SELECT * FROM portfolio_data WHERE portfolio={}".format(portfolio_id)
    cur.execute(sql)

    return cur.fetchall()


def update_all_portfolio_data(conn, portfolio_data):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
     """
    for data in portfolio_data:
        dataset = (data['asset_value'],
                   data['profit_total_absolute'],
                   data['profit_total_relative'],
                   data['profit_today_absolute'],
                   data['profit_today_relative'],
                   data['trailingAnnualDividendRate'],
                   data['trailingAnnualDividendYield'],
                   data['dividend'],
                   data['id'])

        sql = ''' UPDATE portfolio_data
                  SET asset_value = ?, 
                      profit_total_absolute = ?, 
                      profit_total_relative = ?, 
                      profit_today_absolute = ?, 
                      profit_today_relative = ?, 
                      trailingAnnualDividendRate = ?, 
                      trailingAnnualDividendYield = ?, 
                      dividend = ?
                  WHERE asset = ?'''

        cur = conn.cursor()
        cur.execute(sql, dataset)

        conn.commit()
        cur.close()


def update_all_portfolios(conn, portfolios):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
     """
    for data in portfolios:
        dataset = (data['portfolio_value'],
                   data['profit_total_absolute'],
                   data['profit_total_relative'],
                   data['profit_today_absolute'],
                   data['profit_today_relative'],
                   data['dividend'],
                   data['id'])

        sql = ''' UPDATE portfolios
                  SET portfolio_value = ?, 
                      profit_total_absolute = ?, 
                      profit_total_relative = ?, 
                      profit_today_absolute = ?, 
                      profit_today_relative = ?, 
                      dividend = ?
                  WHERE id = ?'''

        cur = conn.cursor()
        cur.execute(sql, dataset)

        conn.commit()
        cur.close()


def select_portfolios_from_user(conn, user_id):
    """
    Query tasks by priority
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    sql = "SELECT * FROM portfolios WHERE user={}".format(user_id)
    cur.execute(sql)

    return cur.fetchall()


def select_portfolio(conn, portfolio_id):
    """
    Query tasks by priority
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    sql = "SELECT * FROM portfolios WHERE id='{}'".format(portfolio_id)
    cur.execute(sql)

    return cur.fetchall()


def select_all_assets(conn):
    """
    select all assets that are not asset_type=4 (cash)
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    sql = "SELECT * FROM assets WHERE asset_type !=4"
    cur.execute(sql)

    return cur.fetchall()


def select_all_assets_from_portfolio(conn, portfolio_id):
    """
    Query tasks by priority
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    sql = 'SELECT * FROM portfolio_data, assets WHERE portfolio_data.asset = assets.id AND portfolio_data.portfolio={} ORDER BY asset_value DESC'.format(
        portfolio_id)

    cur.execute(sql)

    return cur.fetchall()


def select_single_asset_from_portfolio(conn, portfolio_id, asset_id):
    """
    Query tasks by priority
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    sql = 'SELECT * FROM portfolio_data, assets WHERE portfolio_data.asset = assets.id AND portfolio_data.portfolio={} AND assets.id={} ORDER BY asset_value DESC'.format(
        portfolio_id, asset_id)

    #print(sql)
    cur.execute(sql)

    return cur.fetchall()


def select_assets_from_portfolio_grouped_by_sector(conn, portfolio_id):
    """
    Query tasks by priority
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    sql = 'SELECT at.title, sum(portfolio_value) as val ' \
          'FROM portfolios ' \
          'JOIN asset_types at on at.id = portfolios.portfolio_type ' \
          'GROUP BY portfolios.portfolio_type ' \
          'HAVING portfolios.user = {}'.format(portfolio_id)

    cur.execute(sql)

    return cur.fetchall()

def select_all_sectors(conn):
    """
    selects all secotrs. format: id, title
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    sql = 'SELECT * FROM sectors'

    cur.execute(sql)

    return cur.fetchall()


def api_portfolio_insert_stock(conn, data):
    """

    :param form input
    :return:
    """

    # check if stock already in db assets - yes: insert and get id, no: use id
    # check if asset already in portfolio, then update
    # insert into portfolio_data

    cur = conn.cursor()
    sql = "SELECT * FROM assets WHERE symbol='{}'".format(data['symbol'])

    cur.execute(sql)

    res = cur.fetchall()

    if len(res) > 0:
        asset_id = res[0]['id']
    else:
        # insert into asset
        cur = conn.cursor()
        sql = "INSERT INTO assets (symbol, asset_type) VALUES ('{}', {})".format(data['symbol'], data['portfolio_type'])

        cur.execute(sql)

        asset_id = cur.lastrowid

        cur = conn.cursor()
    sql = "INSERT INTO portfolio_data (asset, quantity, buyIn, title, portfolio, sector) VALUES ({}, {}, {}, '{}', {}, {})".format(
        asset_id, data['quantity'], data['buyIn'], data['title'], data['portfolio'], data['sector']
    )
    cur.execute(sql)
    cur.close()
    return 'true'


def api_portfolio_update_stock(conn, data):
    sql = "UPDATE portfolio_data SET buyIn={}, title='{}', portfolio={}, sector={}, quantity={} WHERE asset={}".format(
        data['buyIn'], data['title'], data['portfolio'], data['sector'], data['quantity'], data['id']
    )

    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

    cur.close()
    return data