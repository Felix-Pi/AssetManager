import json

import requests
import difflib

from db import select_portfolios_from_user, select_all_assets_from_portfolio


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


def yahoo_search_request(input, region, lang):
    url = 'http://d.yimg.com/aq/autoc?query={}&region={}&lang={}'.format(
        html_encode(input), region, lang)  # ToDO: return data['ResultSet']['Result'], need to fix every usage
    return requests.get(url).json()


def search_alternative_symbols(symbol, match_ratio=80):
    # get stock title
    data = yahoo_search_request(symbol, 'DE', 'de-DE')
    if data is None or len(data) == 0:
        return []

    title = data['ResultSet']['Result'][0]['name']  # ToDo

    # search for symbols with stock name on us market to get ticker with information
    alternative_symbols = yahoo_search_request(title, 'US', 'en-US')
    alternative_symbols = alternative_symbols['ResultSet']['Result']

    # select tickers with matching title
    result = []
    for symbol in alternative_symbols:
        ratio = int(difflib.SequenceMatcher(None, title.lower(), symbol['name'].lower()).ratio() * 100)
        # print(title.lower(), '|', symbol['name'].lower(), ratio)
        if ratio > match_ratio:
            result.append(symbol)

    return result


def get_usd_eur():
    def send_request():
        url = 'https://query1.finance.yahoo.com/v7/finance/quote?symbols=USDEUR=X'

        data = requests.get(url).json()
        return data['quoteResponse']['result'][0]

    def parse_result(data):
        if data is not None and 'regularMarketPrice' in data:
            return data['regularMarketPrice']

        return float(1)

    data = send_request()
    return parse_result(data)


def export(conn, USER_ID):
    with conn:
        portfolios = select_portfolios_from_user(conn, USER_ID)

        result = {}

        for pf in portfolios:
            print(pf)
            result[pf['title'].lower()] = {
                'title': pf['title'],
                'db': []
            }
            db = result[pf['title'].lower()]['db']

            assets = select_all_assets_from_portfolio(conn, pf['id'])

            print(pf['portfolio_type'], pf)
            if pf['portfolio_type'] == 4:
                for asset in assets:
                    db.append({
                        'title': asset['title'],
                        'value': asset['asset_value'],
                    })
            else:
                for asset in assets:
                    db.append({
                        'symbol': asset['symbol'],
                        'title': asset['title'],
                        'buyin': asset['buyIn'],
                        'amount': asset['quantity'],
                    })

    with open('/Users/felixpieschka/dev/python/PortfolioTicker/data/data.json', 'w') as outfile:
        json.dump([result], outfile)
