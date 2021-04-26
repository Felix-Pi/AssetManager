from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import index
from app.api import portfolio
from app.api import asset
from app.api import render_template
from app.api import other
