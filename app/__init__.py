from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_breadcrumbs import Breadcrumbs
from app.config import Config

app = Flask(__name__, template_folder='../templates/', static_folder='../static/')

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

Breadcrumbs(app)
bootstrap = Bootstrap(app)
login = LoginManager(app)

from app.models.User import *
from app.models.Portfolio import *
from app.models.Asset import *
from app.models.Portfolio_position import *
from app.domain_logic.domain_logic import *

from app.routes.auth import bp as auth_bp
from app.routes.index import bp as index_bp
from app.routes.portfolio import bp as portfolio_bp
from app.routes.asset import bp as asset_bp
from app.routes.api import bp as api_bp
from app.routes.moneyManager import bp as moneyManager_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(index_bp, url_prefix='/index')
app.register_blueprint(portfolio_bp, url_prefix='/portfolio')
app.register_blueprint(asset_bp, url_prefix='/asset')
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(moneyManager_bp, url_prefix='/moneyManager')

from app import routes

app.logger.setLevel(Config.log_level)
# print(app.url_map)
# app.logger.info('Routes: {}'.format(param))
