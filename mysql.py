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


def select_all_asset_types(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute('SELECT * FROM asset_types')

    rows = cur.fetchall()

    print(rows)
    # for row in rows:
    #    print(row)


def select_all_symbols(conn):
    """
    Query tasks by priority
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    # cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))

    allowed_types = 1
    # sql = 'SELECT a.symbol, a.title, a.buyin, a.quantity, at.title as asset_type FROM static a JOIN asset_types at on at.id = a.asset_type'
    cur.execute('SELECT * FROM assets')

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

    sql = 'SELECT pd.id, pd.quantity, pd.buyIn, a.* ' \
          'FROM portfolio_data pd ' \
          'JOIN assets a on a.id = pd.asset'
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


def select_portfolios_from_user(conn, user_id):
    """
    Query tasks by priority
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    sql = "SELECT * FROM portfolios WHERE user='{}'".format(user_id)
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


def select_assets_from_portfolio(conn, portfolio_id):
    """
    Query tasks by priority
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    sql = 'SELECT * FROM portfolio_data, assets WHERE portfolio_data.asset = assets.id AND portfolio_data.portfolio={} ORDER BY asset_value DESC'.format(portfolio_id)

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

def select_sectordata_from_portfolio_grouped_by_sector(conn, portfolio_id):
    """
    Query tasks by priority
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    sql = 'SELECT b.title, sum(asset_value) as val ' \
          'FROM portfolio_data ' \
          'JOIN sectors b on b.id = portfolio_data.sector ' \
          'GROUP BY portfolio_data.sector ' \
          'HAVING portfolio_data.portfolio = {}'.format(portfolio_id)

    cur.execute(sql)

    return cur.fetchall()
