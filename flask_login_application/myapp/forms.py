"""All the forms which will be used in myapp"""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class BaseAuthForm(FlaskForm):
    """Base form haivng common form fields"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(BaseAuthForm):
    """User login form. Inherits basic fields from BaseAuthForm"""
    submit = SubmitField('Sign In')


class SignupForm(BaseAuthForm):
    """User Signup form. Inherits basic fields from BaseAuthForm"""
    submit = SubmitField('Sign up')
