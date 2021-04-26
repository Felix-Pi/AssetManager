import logging

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

USER_ID = 1

app = Flask(__name__, template_folder='../templates/', static_folder='../static/')

app.config.from_object(Config)

from flask.logging import default_handler

default_handler.setFormatter(logging.Formatter(
    ' * [%(levelname)s][%(filename)s:%(lineno)d]: %(message)s'
))

app.logger.setLevel(logging.DEBUG)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes
from app.models.User import *
from app.models.Portfolio import *
from app.models.Asset import *
from app.models.Portfolio_position import *

from app.index import bp as index_bp
from app.portfolio import bp as portfolio_bp
from app.asset import bp as asset_bp
from app.api import bp as api_bp

app.register_blueprint(index_bp, url_prefix='/index')
app.register_blueprint(portfolio_bp, url_prefix='/portfolio')
app.register_blueprint(asset_bp, url_prefix='/asset')
app.register_blueprint(api_bp, url_prefix='/api')

# app.logger.info('Routes: '.format(print(app.url_map)))
