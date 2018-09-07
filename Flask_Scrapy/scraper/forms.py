from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(id='username', label='Username', validators=[DataRequired()])
    password = PasswordField(id='password', label='Password', validators=[DataRequired()])
    remember_me = BooleanField(id='remember', default=False)


class RegisterForm(FlaskForm):
    username = StringField(id='username', label='Username', validators=[DataRequired()])
    password = PasswordField(id='password', label='Password', validators=[DataRequired()])
    re_password = PasswordField(id='re_password', label='Re-Enter Password', validators=[DataRequired()])


class CreateBlog(FlaskForm):
    title = StringField(id='title', validators=[DataRequired()])
    body = TextAreaField(id='body', validators=[DataRequired()])
