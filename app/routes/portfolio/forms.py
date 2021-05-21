from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, SelectField
from wtforms.fields.html5 import EmailField, IntegerField, DecimalField, DateField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email, InputRequired

from app import db, Asset_types, Transaction_types, Portfolio, app


class AddTransactionForm(FlaskForm):
    today = datetime.now()  # .strftime('%d.%m.%Y')

    portfolio = SelectField('Portfolio', validators=[DataRequired()],
                            choices=[])

    # transaction_type = SelectField('Transaction Type', validators=[DataRequired()],
    #                                choices=[(a.id, a.title) for a in db.session.query(Transaction_types).all()])

    symbol = StringField('Symbol', validators=[])
    price = DecimalField('Price', validators=[DataRequired()])
    quantity = DecimalField('Quantity', validators=[DataRequired()])
    fee = DecimalField('Fee', validators=[InputRequired()])
    date = DateField('Date', validators=[DataRequired()], default=today, format='%d.%m.%y')
    submit = SubmitField('Add transaction')
