from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class BaseAuthForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(BaseAuthForm):
    submit = SubmitField('Sign In')


class SignupForm(BaseAuthForm):
    submit = SubmitField('Sign up')
