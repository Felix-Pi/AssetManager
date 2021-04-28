from flask import Blueprint

bp = Blueprint('api', __name__)

from app.routes.api import asset
from app.routes.api import index
from app.routes.api import other
from app.routes.api import portfolio
from app.routes.api import render_template

