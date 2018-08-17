from flask import flash, render_template, redirect
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy.exc import IntegrityError
from myapp import app, db, login_manager
from myapp.forms import LoginForm, SignupForm
from myapp.models import User

login_manager.login_view = '/login'


def is_authorized(func):
    """Return to profile page if user is already logged in."""

    def authenticate(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect("/profile")
        else:
            return func(*args, **kwargs)

    authenticate.__name__ = func.__name__
    return authenticate


@app.route('/')
@app.route('/index')
@is_authorized
def index():
    """Return the index.html page"""
    return render_template('index.html', title='Home')


@app.route('/login', methods=["POST", "GET"])
@is_authorized
def login():
    """ if form is submitted, login the user if the user credentials are correct
    otherwise return the login page
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid user credentials.")
            return render_template("login.html",
                                   form=form)
        else:
            login_user(user)
            flash("login successful")
            return redirect("/profile")
    return render_template("login.html", form=form)


@app.route('/signup', methods=["GET", "POST"])
@is_authorized
def signup():
    """ if form is submitted, register the user if the user credentials are correct
        otherwise return the signup page
        """
    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data)
        new_user.set_password(form.password.data)
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            flash("Registration failed!")
            return render_template('signup.html',
                                   title="signup",
                                   form=form)

        form = LoginForm()
        flash("Registration successful")
        return render_template('index.html',
                               title="Home",
                               form=form)
    else:
        return render_template('signup.html', title="signup", form=form)


@app.route('/profile')
@login_required
def profile():
    """Return the profile page if user is logged in."""
    return render_template("profile.html")


@app.route('/logout')
def logout():
    """Logout user and then redirect to index page."""
    if current_user.is_authenticated:
        logout_user()

    return redirect("/index")
