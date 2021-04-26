from flask import render_template

from app.api import *
from app.domain_logic.newsfeed import get_news_for_ticker


@bp.route('/render_template/news/<string:symbol>', methods=['GET'])
def get_news(symbol):
    templateData = {
        'news': get_news_for_ticker(symbol),
    }
    return render_template('modules/newsfeed/newsfeed_inner.html', **templateData)

