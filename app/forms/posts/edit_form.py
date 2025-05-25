from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired, Length, NumberRange

class EditForm(FlaskForm):
    title = StringField("title", validators=[DataRequired(), Length(min=5, max=20)])
    content = StringField("content", validators=[DataRequired()])
