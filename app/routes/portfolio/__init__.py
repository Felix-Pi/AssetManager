from flask import Blueprint

bp = Blueprint('portfolio', __name__)

from app.routes.portfolio import routes