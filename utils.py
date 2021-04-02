import json

import requests


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
        html_encode(input), region, lang)
    return requests.get(url).json()
