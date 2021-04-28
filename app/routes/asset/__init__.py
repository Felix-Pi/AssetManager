from flask import Blueprint

bp = Blueprint('asset', __name__)

from app.routes.asset import routes