from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostFrom(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2, max=10)])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Add Post")