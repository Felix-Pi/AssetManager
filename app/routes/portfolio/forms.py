from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, SelectField
from wtforms.fields.html5 import EmailField, IntegerField, DecimalField, DateField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Email


# class MyFloatField(DecimalField):
#     def process_formdata(self, valuelist):
#         if valuelist:
#             try:
#                 self.data = float(valuelist[0].replace(',', '.'))
#             except ValueError:
#                 self.data = None
#                 raise ValueError(self.gettext('Not a valid float value'))
from app import db, Asset_types


class AddTransactionForm(FlaskForm):
    type = SelectField('Type', validators=[DataRequired()], choices=[(a.id, a.type) for a in db.session.query(Asset_types).all()])


    symbol = StringField('Symbol', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    quantity = DecimalField('Quantity', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Add transaction')
