from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp, Optional
from wtforms.fields.simple import BooleanField, TextAreaField
from .models import User
from flask_wtf.file import FileAllowed, FileField
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=16),
        Regexp('^[A-Za-z][A-Za-z0-9_-]*$', message="Username must contain only letters, numbers, and underscores.")
    ])
    
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message="Password must be at least 6 characters.")
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match.")
    ])
    
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered.')
        
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log In')
    
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=16),
        Regexp('^[A-Za-z][A-Za-z0-9_-]*$', message="Username must contain only letters, numbers, and underscores.")
    ])
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    image_file = FileField('Update Profile Picture', validators=[FileAllowed(['png', 'jpeg', 'jpg'])])
    about_me = TextAreaField('About Me', validators=[Length(max=670)])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already registered.')
            
            
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=4, max=16)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')
    
    def validate_old_password(self, current_password):
        if not current_user.check_password(current_password.data):
            raise ValidationError('Your password is incorrect.')