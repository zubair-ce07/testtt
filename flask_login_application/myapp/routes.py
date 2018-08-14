from flask import render_template, redirect
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy.exc import IntegrityError
from myapp import app, db
from myapp.forms import LoginForm, SignupForm
from myapp.models import User


def is_authorized(func):
    """Return to profile page if user is already logged in."""

    def authenticate(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect("/profile")
        else:
            return func(*args, **kwargs)

    authenticate.__name__ = func.__name__
    return authenticate


def login_required(func):
    """Return to login  page if user is not already logged in."""

    def authenticate(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect("/login")
        else:
            return func(*args, **kwargs)

    return authenticate


@app.route('/')
@app.route('/index')
@is_authorized
def index():
    login_form = LoginForm()
    return render_template('index.html', title='Home', form=login_form)


@app.route('/login', methods=["POST", "GET"])
@is_authorized
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return render_template("index.html",
                                   error=True,
                                   form=form)
        else:
            login_user(user)
        return redirect("/profile")
    return render_template("index.html", form=form)


@app.route('/signup', methods=["GET", "POST"])
@is_authorized
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            return render_template('signup.html', title="signup",
                                   form=form, error="Invalid Data.")

        form = LoginForm()
        return render_template('index.html', title="Home",
                               registration_successful=True, form=form)
    else:
        return render_template('signup.html', title="signup", form=form)


@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html")


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()

    return redirect("/index")
