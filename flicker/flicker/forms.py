from flask_wtf import Form
from wtforms import TextField, SubmitField, PasswordField, \
    BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, Email


class AddPostForm(Form):
    tag = TextField('tag', validators=[DataRequired()])


class SignUpForm(Form):
    username = TextField('User Name',
                         validators=[DataRequired(), Length(min=4)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sign Up')


class SignInForm(Form):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=6, max=30)])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Sign In')
