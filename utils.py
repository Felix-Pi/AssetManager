import json

import requests


def yahoo_search_request(input):
    url = 'http://d.yimg.com/aq/autoc?query={}&region=DE&lang=de-DE'.format(
        input)
    data = requests.get(url).content
    return data
