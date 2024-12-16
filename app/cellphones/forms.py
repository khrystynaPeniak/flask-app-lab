from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from .models import CellphoneCategory

class CellphoneForm(FlaskForm):
    name = StringField("Cellphone's name", 
                      validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('description')
    price = FloatField('Price', 
                      validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Category', 
                         coerce=int,
                         validators=[DataRequired()])
    submit = SubmitField('Add')

    def all_categories(self):
        self.category.choices = [(category.id, category.category_name) 
                                for category in CellphoneCategory.query.all()]

class SearchFilterForm(FlaskForm):
    search = StringField('Search for name', validators=[Length(max=100)])
    sort_by = SelectField('Sort by', choices=[
        ('name', 'Name'),
        ('price', 'Price'),
        ('category', 'Category')
    ])
    sort_order = SelectField('Order', choices=[
        ('asc', 'Ascending'),
        ('desc', 'Descending')
    ])
    category = SelectField('Filter by Category', coerce=int, choices=[], default='')
    submit = SubmitField('Apply')

    def all_categories(self):
        categories = [(category.id, category.category_name) 
                     for category in CellphoneCategory.query.all()]
        self.category.choices = [(0, 'All Categories')] + categories