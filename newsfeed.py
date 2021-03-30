from datetime import datetime

import requests


# ToDo: amount of headlines
def get_news_for_ticker(symbols):
    url = 'https://api.rss2json.com/v1/api.json?rss_url=http://feeds.finance.yahoo.com/rss/2.0/headline?s='

    max_description_length = 500

    if len(symbols) > 0 and symbols[0] is None:
        return None
    if isinstance(symbols, list):
        symbols = ','.join(symbols)

    req = requests.get(url + symbols + '&lang=de-DE,en-US').json()

    if req['status'] == 'ok':
        for event in req['items']:
            # shorten description
            if len(event['description']) > max_description_length:
                event['description_prev'] = event['description'][:max_description_length] + '...'
            else:
                event['description_prev'] = event['description']

            # format pubDate
            pubDate = datetime.strptime(event['pubDate'], '%Y-%m-%d %H:%M:%S')
            event['pubDate'] = pubDate.strftime("%m.%d.%Y, %H:%M")
        return req['items']

    return None
