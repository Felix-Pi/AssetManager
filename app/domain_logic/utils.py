import collections
import os
from datetime import datetime, timedelta

from flask import make_response, jsonify

from app import app


def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
        ("'", '&#39;'),
        ('"', '&quot;'),
        ('>', '&gt;'),
        ('<', '&lt;'),
        ('&', '&amp;')
    )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s


def html_encode(html):
    """Returns the given HTML with ampersands, quotes and carets encoded."""
    return html.replace(" ", '&quot;')


def return_error(code, description):
    return make_response(jsonify(description), code)


def delete_key_from_dict(dict, key):
    if isinstance(key, str):
        if key in dict:
            del dict[key]
    if isinstance(key, list):
        for k in key:
            if k in dict:
                del dict[k]

    return dict


def get_csv_data(domain, id, period, interval):
    """
    reads csv data from storage.
    :param domain:
    :param id:
    :param period:
    :param interval:
    :return: File, File creation Time, bool refresh (refresh file data)
    """
    file = 'data/csv/{}/{}_{}_{}_{}.csv'.format(domain, domain, id, period, interval)
    refresh = True
    creation_time = None

    if os.path.isfile(file):
        stat = os.stat(file)
        creation_time = datetime.fromtimestamp(stat.st_mtime)

        if '1d' == period or '2d' == period:
            condition_time = datetime.now() - timedelta(hours=1)
        else:
            condition_time = datetime.now() - timedelta(days=1)

        if creation_time > condition_time:
            refresh = False

        app.logger.info('Loading file: {}, refresh: {}'.format(file, refresh))
        return file, creation_time, refresh

    app.logger.info('Loading file: {} [NOT FOUND], refresh: {}'.format(file, refresh))
    return None, refresh, creation_time


def filter_asset_name(name):
    blacklist = [',', 'Inc.', 'Inc', 'S.A.', 'SE', '& Co. KGaA', ' AG', 'N.V.', 'ltd.', 'Ltd.', 'ltd',
                 'Limited', 'plc',
                 'Corp.', 'Holdings', 'Holding', 'Corporation', 'Aktiengesellschaft', '.com', '.dl-0001',
                 'UCITS', 'ETF', 'USD', '(Dist)', '(Acc)', 'Eur', 'iShares']

    for substr in blacklist:
        name = name.replace(substr.upper(), '')
        name = name.replace(substr, '')

    name = name.replace('amp;', '')

    return name
