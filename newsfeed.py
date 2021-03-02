import requests


def get_news_for_ticker(symbols):
    url = 'https://api.rss2json.com/v1/api.json?rss_url=http://feeds.finance.yahoo.com/rss/2.0/headline?s='

    if len(symbols) > 0 and symbols[0] is None:
        return None
    if isinstance(symbols, list):
        symbols = ','.join(symbols)

    print(symbols)
    req = requests.get(url + symbols).json()

    if req['status'] == 'ok':
        return req['items']

    return None
