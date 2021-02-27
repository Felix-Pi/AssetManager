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
    # sql = 'SELECT a.symbol, a.title, a.buyin, a.quantity, at.title as asset_type FROM assets a JOIN asset_types at on at.id = a.asset_type'
    cur.execute('SELECT * FROM assets')

    return cur.fetchall()

def select_all_portfolios(conn):
    """
    Query tasks by priority
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    # cur.execute("SELECT * FROM tasks WHERE priority=?", (priority,))

    allowed_types = 1
    # sql = 'SELECT a.symbol, a.title, a.buyin, a.quantity, at.title as asset_type FROM assets a JOIN asset_types at on at.id = a.asset_type'
    cur.execute('SELECT * FROM portfolios')

    return cur.fetchall()
