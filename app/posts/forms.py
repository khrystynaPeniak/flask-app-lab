from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField, DateField, SelectField
from wtforms.validators import DataRequired, Length

CATEGORIES = [('tech', 'Tech'), ('science', 'Science'), ('lifestyle', 'Lifestyle')]

class PostFrom(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2, max=10)])
    content = TextAreaField("Content", render_kw={"rows": 5, "cols": 40}, validators=[DataRequired()])
    is_active = BooleanField("Is this post active?", default=True)
    publish_date = DateField("Publish date", format='%Y-%m-%d', validators=[DataRequired()])
    category = SelectField("Category", choices=CATEGORIES, validators=[DataRequired()])
    submit = SubmitField("Add Post")