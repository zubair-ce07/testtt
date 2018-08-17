from flask import Flask, request, session, redirect, url_for, render_template, \
    flash, jsonify
from .models import User, Posts, db
from .forms import AddPostForm, SignUpForm, SignInForm, AboutUserForm
from blog import app

@app.route('/')
def index():
    posts = Posts.query.all()
    user = User.query.all()
    return render_template('index.html', posts=posts, user=user)

@app.route('/posts')
def show_posts():
    user_id = session.get('user_available')
    if user_id is None:
        session['user_available'] = None
    if session['user_available']:
        posts = Posts.query.all()
        user = User.query.all()
        return render_template('posts.html', posts=posts, user=user)
    flash('User is not Authenticated')
    return redirect(url_for('index'))


@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if session['user_available']:
        blogpost = AddPostForm(request.form)
        us = User.query.filter_by(username=session['current_user']).first()
        if request.method == 'POST':
            bp = Posts(blogpost.title.data, blogpost.description.data, us.uid)
            db.session.add(bp)
            db.session.commit()
            flash('Post Created Succesfully')
            return redirect(url_for('index'))
        return render_template('add.html', blogpost=blogpost)
    flash('User is not Authenticated')
    return redirect(url_for('index'))


@app.route('/delete/<pid>/<post_owner>', methods=('GET', 'POST'))
def delete_post(pid, post_owner):
    if session['current_user'] == post_owner:
        post = Posts.query.get(pid)
        db.session.delete(post)
        db.session.commit()
        flash('Post Deleted Succesfully')
        return redirect(url_for('index'))
    flash('You are not a valid user to Delete this Post')
    return redirect(url_for('index'))


@app.route('/update/<pid>/<post_owner>', methods=('GET', 'POST'))
def update_post(pid, post_owner):
    if session['current_user'] == post_owner:
        post = Posts.query.get(pid)
        blogpost = AddPostForm(obj=post)
        if request.method == 'POST':
            bpost = Posts.query.get(pid)
            bpost.title = blogpost.title.data
            bpost.description = blogpost.description.data
            db.session.commit()
            flash('Post Updated Succesfully')
            return redirect(url_for('index'))
        return render_template('update.html', blogpost=blogpost)
    flash('You are not a valid user to Edit this Post')
    return redirect(url_for('show_posts'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signupform = SignUpForm(request.form)
    if request.method == 'POST':
        reg = User(signupform.username.data, signupform.password.data, \
                   signupform.email.data)
        db.session.add(reg)
        db.session.commit()
        return redirect(url_for('signin'))
    return render_template('signup.html', signupform=signupform)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    signinform = SignInForm()
    if request.method == 'POST':
        em = signinform.email.data
        log = User.query.filter_by(email=em).first()
        if log.password == signinform.password.data:
            current_user = log.username
            session['current_user'] = current_user
            session['user_available'] = True
            return redirect(url_for('index'))
    return render_template('signin.html', signinform=signinform)


@app.route('/logout')
def logout():
    session.clear()
    session['user_available'] = False
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
