from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.fields.datetime import DateTimeLocalField
from datetime import datetime as dt

CATEGORIES = [('tech', 'Tech'), ('science', 'Science'), ('lifestyle', 'Lifestyle')]

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2, max=10)])
    content = TextAreaField("Content", render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])
    is_active = BooleanField("Is this post active?", default=True)
    publish_date = DateTimeLocalField("Publish date", format='%Y-%m-%dT%H:%M', default=dt.now(), validators=[DataRequired()])
    category = SelectField("Category", choices=CATEGORIES, validators=[DataRequired()])
    submit = SubmitField("Add Post")