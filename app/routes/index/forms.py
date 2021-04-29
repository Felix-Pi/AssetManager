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


class AddPortfolio(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    type = IntegerField('Type', validators=[DataRequired()])
    submit = SubmitField('Add transaction')
