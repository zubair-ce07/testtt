import os
import random
import string

from flask import request, session, redirect, url_for, \
    render_template, flash
from flicker import app
from sqlalchemy import desc
from werkzeug.security import check_password_hash, generate_password_hash

from .forms import AddPostForm, SignUpForm, SignInForm
from .models import User, Posts, Tag, Follow, db

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    if session.get('user_available') and session['user_available']:
        posts_data_list = db.session.query(Posts.pid, Posts.post_privacy,
                                           Posts.image_url, Posts.puid,
                                           User.uid, User.username).filter(
            Posts.puid == User.uid).order_by(desc(Posts.pid))
        users_list = db.session.query(Follow.followed_username,
                                      Follow.followed_userid).filter(
            Follow.following_userid == session['current_user_id'])
        followed_users_list = []
        for user in users_list:
            followed_users_list.append(user.followed_userid)
        return render_template('index.html', posts_data_list=posts_data_list,
                               followed_users_list=followed_users_list)
    flash('User is not Authenticated')
    return redirect(url_for('signin'))


def allowed_file(filename):
    allowed_extensions = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/wall', methods=['GET'])
def user_wall():
    if session.get('user_available') and session['user_available']:
        posts_data_list = db.session.query(Posts.pid, Posts.post_privacy,
                                           Posts.image_url, Posts.puid).filter(
            Posts.puid == session['current_user_id']).order_by(desc(Posts.pid))
        following_users = db.session.query(Follow).filter(
            Follow.following_userid == session['current_user_id']).all()
        return render_template('user_wall.html',
                               posts_data_list=posts_data_list,
                               following_users=following_users,
                               current_user_id=session['current_user_id'],
                               current_user=session['current_user']
                               )


def generate_id(size=7, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def append_id(filename):
    name, ext = os.path.splitext(filename)
    return "{name}_{uid}{ext}".format(name=name, uid=generate_id(), ext=ext)


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if session.get('user_available') and session['user_available']:
        blog_post = AddPostForm(request.form)
        user = User.query.filter_by(username=session['current_user']).first()
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                file_name = append_id(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                         file_name)
                file.save(file_path)
                privacy_type = request.form['privacy']
                post = Posts("uploads/" + file_name,
                             privacy_type, user.uid)
                db.session.add(post)
                db.session.commit()
                save_post_tags(blog_post.tag.data, post.pid)
                flash('Post Created Succesfully')
                return redirect(url_for('index'))
        return render_template('add.html', blog_post=blog_post)
    flash('User is not Authenticated')
    return redirect(url_for('signin'))


def save_post_tags(tags_list, post_id):
    tags_list = tags_list.split(" ")
    for tag in tags_list:
        tag_obj = Tag(tag, post_id)
        db.session.add(tag_obj)
        db.session.commit()


@app.route('/user/<user_id>/<username>', methods=('GET', 'POST'))
def user_profile(user_id, username):
    if request.method == 'POST':
        follow_status_form = request.form.get('follow_status_form')
        update_follow_status(user_id, follow_status_form, username)

    follow_status = check_follow_status(user_id)
    user_data = db.session.query(User).filter(User.uid == user_id).all()
    posts_data_list = db.session.query(Posts.pid, Posts.post_privacy,
                                       Posts.image_url, Posts.puid).filter(
        Posts.puid == user_id).order_by(desc(Posts.pid))
    following_users = db.session.query(Follow).filter(
        Follow.following_userid == user_id).all()
    return render_template('user_wall.html',
                           posts_data_list=posts_data_list,
                           following_users=following_users,
                           follow_status=follow_status,
                           user_data=user_data,
                           current_user_id=user_id,
                           current_user=username
                           )


@app.route('/search_user', methods=('GET', 'POST'))
def search_user():
    if request.method == 'POST':
        search_element = request.form.get('search_elem')
        user_data_list = db.session.query(User).filter(
            User.username.like('%' + search_element + '%')).all()
        return render_template('user_list.html', users_list=user_data_list)


def update_follow_status(profile_user_id, follow_status, profile_username):
    current_user_id = session['current_user_id']
    profile_user_id = int(profile_user_id)
    if follow_status == "1":
        follow_instance = db.session.query(Follow).filter(
            Follow.following_userid == current_user_id and
            Follow.followed_userid == profile_user_id).first()
        db.session.delete(follow_instance)
        db.session.commit()
    if follow_status == "0":
        follow = Follow(current_user_id, profile_user_id,
                        session['current_user'], profile_username)
        db.session.add(follow)
        db.session.commit()


def check_follow_status(profile_user_id):
    current_user_id = session['current_user_id']
    profile_user_id = int(profile_user_id)
    follow_status = db.session.query(Follow).filter(
        Follow.following_userid == current_user_id,
        Follow.followed_userid == profile_user_id).all()
    if follow_status:
        return True
    else:
        return False


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignUpForm(request.form)
    if request.method == 'POST':
        if validate_username(signup_form.username.data) is False:
            flash('Username Already Exists')
            print("Email Invalid")
            return redirect(url_for('signup'))
        if validate_user_email(signup_form.email.data) is False:
            flash('Email Already Exists')
            print("username Invalid")
            return redirect(url_for('signup'))
        else:
            file = request.files['file']
            if file and allowed_file(file.filename):
                file_name = append_id(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                         file_name)
                file.save(file_path)
            register_user = User(signup_form.username.data,
                                 generate_password_hash(
                                     signup_form.password.data),
                                     "uploads/" + file_name,
                                 signup_form.email.data)
            db.session.add(register_user)
            db.session.commit()
            flash('User Registered Succesfully')
            return redirect(url_for('signin'))
    return render_template('signup.html', signup_form=signup_form)


def validate_user_email(user_email):
    log_user_email = User.query.filter_by(email=user_email).first()
    if log_user_email:
        return False
    else:
        return True


def validate_username(username):
    log_user_username = User.query.filter_by(username=username).first()
    if log_user_username:
        return False
    else:
        return True


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    signin_form = SignInForm()
    if request.method == 'POST':
        signin_form_email = signin_form.email.data
        log_user = User.query.filter_by(email=signin_form_email).first()
        if log_user:
            if check_password_hash(log_user.password,
                                   signin_form.password.data):
                current_user = log_user.username
                session['current_user'] = current_user
                session['current_user_id'] = log_user.uid
                session['user_available'] = True
                return redirect(url_for('index'))
            else:
                flash('Incorrect Password Entered')
                return render_template('signin.html', signin_form=signin_form)
        else:
            flash('Email Not Registered')
            return render_template('signin.html', signin_form=signin_form)
    return render_template('signin.html', signin_form=signin_form)


@app.route('/logout')
def logout():
    session.clear()
    session['user_available'] = False
    return redirect(url_for('index'))
