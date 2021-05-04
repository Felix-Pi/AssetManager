from flask import Blueprint
from flask_breadcrumbs import default_breadcrumb_root

bp = Blueprint('asset', __name__)
default_breadcrumb_root(bp, '.')
from app.routes.asset import routes