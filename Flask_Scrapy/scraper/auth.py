import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

from . import validate_password
from .database import db_session
from .forms import LoginForm, RegisterForm
from .models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    register_user = RegisterForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        re_password = request.form['re_password']
        error = validate_password.password_check(password)

        if not username:
            error = 'Username is required.'

        elif db_session.query(User.username).filter(User.username == username).first() is not None:
            error = 'User {} is already registered.'.format(username)

        elif password != re_password:
            error = "Password doesn't match"

        if error is None:
            user = User(username=username, password=generate_password_hash(password))
            db_session.add(user)
            db_session.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html',
                           form=register_user)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    login_user = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = db_session.query(User).filter(User.username == username).first()

        if user is None:
            error = 'Username does not exist'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('item.index'))

        flash(error)

    return render_template('auth/login.html',
                           form=login_user)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = db_session.query(User).filter(User.id == user_id).first()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
