from flask import Blueprint

bp = Blueprint('asset', __name__)

from app.asset import routes