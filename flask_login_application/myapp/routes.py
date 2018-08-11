from flask import render_template, redirect
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_user, logout_user
from myapp import app, db
from myapp.forms import LoginForm,SignupForm
from myapp.models import User


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect("/profile")

    login_form = LoginForm()
    return render_template('index.html', title='Home', form=login_form)


@app.route('/login', methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect("/profile")

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return render_template("index.html", error = True,
                                   form=form)
        else:
            login_user(user)
        return redirect("/profile")
    return render_template("index.html", form=form)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect("/profile")

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
def profile():
    if not current_user.is_authenticated:
        form = LoginForm()
        return render_template("index.html", form=form)
    else:
        return render_template("profile.html")


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()

    return redirect("/index")
