from flask import url_for
from flask_login import current_user
from werkzeug.utils import redirect

from app import app


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    else:
        return redirect(url_for('auth.login'))
