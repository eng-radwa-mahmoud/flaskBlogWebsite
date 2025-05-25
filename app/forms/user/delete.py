from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange

class DeleteForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), Length(min=8, max=20)])

