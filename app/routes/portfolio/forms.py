from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField
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


class AddTransactionForm(FlaskForm):
    type = IntegerField('Type', validators=[DataRequired()])
    symbol = StringField('Symbol', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    quantity = DecimalField('Quantity', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Add transaction')
