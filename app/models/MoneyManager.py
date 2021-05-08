import json
import re
from datetime import datetime

from dateutil.relativedelta import relativedelta

from app import db


class MoneyManager(db.Model):
    symbol = db.Column(db.String(64), primary_key=True, unique=True)

class Asset_types(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(64))
