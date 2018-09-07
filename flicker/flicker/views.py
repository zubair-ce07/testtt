""" Contains views for rendering web pages """
from flask import request, redirect, url_for, \
    render_template, flash
from werkzeug.security import check_password_hash, generate_password_hash

from flicker import app
from .forms import AddPostForm, SignUpForm, SignInForm
from .utils import *

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET', 'POST'])
def index():
    """ Renders index page
        update logged in user's Likes and Comments
    """
    if session.get('user_available'):
        if request.method == 'POST':
            if request.form.get("like_status"):
                post_id = int(request.form.get("post_id"))
                like_status = request.form.get("like_status")
                update_post_like_status(post_id, like_status)
            elif request.form.get("post_id"):
                post_id = int(request.form.get("post_id"))
                comment_text = request.form.get("comment_text")
                add_post_comment(post_id, comment_text)
                flash('Successfully Commented on Post')
            else:
                search_tag = request.form.get("tag")
                posts_data_list, user_likes = collect_tag_posts(search_tag)
                return render_template('index.html',
                                       posts_data_list=posts_data_list,
                                       user_likes=user_likes)
        allowed_posts, user_likes = collect_allowed_posts()
        return render_template('index.html',
                               posts_data_list=allowed_posts,
                               user_likes=user_likes)
    flash('User is not Authenticated')
    return redirect(url_for('signin'))


@app.route('/delete/<pid>', methods=['GET'])
def delete_post(pid):
    """Delete Logged in User's Post"""
    if session.get('user_available'):
        post = Post.query.get(pid)
        if post.user.uid == int(session['current_user_id']):
            os.remove(
                os.path.join(UPLOAD_FOLDER, post.image_url.split('/')[-1]))
            db.session.delete(post)
            db.session.commit()
            flash('Post Deleted Successfully')
            return redirect(url_for('index'))
        flash('You are not a valid user to Delete this Post')
        return redirect(url_for('index'))

    flash('User is not Authenticated')
    return redirect(url_for('signin'))


@app.route('/post/<post_id>', methods=['GET', 'POST'])
def post_detail_view(post_id):
    """ Shows Detail view of Post """
    if session.get('user_available'):
        if request.method == 'POST':
            comment_id = request.form.get("comment_id")
            delete_user_comment(comment_id)
        post_id = int(post_id)
        post_data = Post.query.filter(
            Post.pid == int(post_id)
        ).first()
        return render_template('post_detail_view.html',
                               post_data=post_data)
    else:
        flash('User is not Authenticated')
        return redirect(url_for('signin'))


@app.route('/wall', methods=['GET'])
def user_wall():
    """Renders User Wall"""
    if session.get('user_available'):
        user_data = User.query.filter(
            User.uid == session['current_user_id']).first()
        return render_template('user_wall.html', user_data=user_data)
    flash('User is not Authenticated')
    return redirect(url_for('signin'))


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    """ Adds new Post """
    if session.get('user_available'):
        blog_post = AddPostForm(request.form)
        user = User.query.filter_by(username=session['current_user']).first()
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                file_name = append_random_string(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                         file_name)
                file.save(file_path)
                privacy_type = request.form['privacy']
                post = Post("uploads/" + file_name,
                            privacy_type, user.uid)
                db.session.add(post)
                db.session.commit()
                save_post_tags(blog_post.tag.data, post.pid)
                flash('Post Created Successfully')
                return redirect(url_for('index'))
            flash('Invalid File')
            return redirect(url_for('add_post'))
        return render_template('add.html', blog_post=blog_post)
    flash('User is not Authenticated')
    return redirect(url_for('signin'))


@app.route('/user/<user_id>', methods=('GET', 'POST'))
def user_profile(user_id):
    """Renders Any User's Profile"""
    if session.get('user_available'):
        if request.method == 'POST':
            follow_status_form = request.form.get('follow_status_form')
            update_follow_status(user_id, follow_status_form)

        follow_status = check_follow_status(user_id)
        user_data = User.query.filter(User.uid == user_id).first()
        return render_template('user_wall.html',
                               user_data=user_data,
                               follow_status=follow_status)
    flash('User is not Authenticated')
    return redirect(url_for('signin'))


@app.route('/search_user', methods=('GET', 'POST'))
def search_user():
    """ Search User """
    if session.get('user_available'):
        if request.method == 'POST':
            search_element = request.form.get('search_elem')
            user_data_list = db.session.query(User).filter(
                User.username.like('%' + search_element + '%')).filter(
                User.uid != int(session['current_user_id'])).all()
            return render_template('user_list.html', users_list=user_data_list)
        return render_template('user_list.html', users_list=[])
    flash('User is not Authenticated')
    return redirect(url_for('signin'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """SignUp User """
    signup_form = SignUpForm(request.form)
    if request.method == 'POST':
        if not validate_username(signup_form.username.data):
            flash('Username Already Exists')
            return redirect(url_for('signup'))
        if not validate_user_email(signup_form.email.data):
            flash('Email Already Exists')
            return redirect(url_for('signup'))
        else:
            file = request.files['file']
            if file and allowed_file(file.filename):
                file_name = append_random_string(file.filename)
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
                flash('User Registered Successfully')
                return redirect(url_for('signin'))
            flash('File Not Allowed')
            return redirect(url_for('signup'))
    return render_template('signup.html', signup_form=signup_form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """SignIn User"""
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
            flash('Incorrect Password Entered')
            return render_template('signin.html', signin_form=signin_form)
        flash('Email Not Registered')
        return render_template('signin.html', signin_form=signin_form)
    return render_template('signin.html', signin_form=signin_form)


@app.route('/logout')
def logout():
    """Logout User"""
    session.clear()
    session['user_available'] = False
    return redirect(url_for('index'))
