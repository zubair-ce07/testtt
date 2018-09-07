import datetime

from flask_sqlalchemy import SQLAlchemy

from flicker import app

db = SQLAlchemy(app)


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    profile_image_url = db.Column(db.String(1000))
    email = db.Column(db.String(50), unique=True)
    date_of_reg = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, username, password, profile_image_url, email):
        self.username = username
        self.password = password
        self.profile_image_url = profile_image_url
        self.email = email


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(50))
    post_id = db.Column(db.Integer, db.ForeignKey('post.pid'))
    post = db.relationship('Post',
                           backref=db.backref('tag', lazy=True,
                                              cascade="all, delete-orphan"))

    def __init__(self, tag, post_id):
        self.tag = tag
        self.post_id = post_id


class Follow(db.Model):
    Follow = 1
    Un_Follow = 0
    follower_userid = db.Column(db.Integer, db.ForeignKey('user.uid'),
                                primary_key=True)
    following_userid = db.Column(db.Integer, db.ForeignKey('user.uid'),
                                 primary_key=True)
    follower_user = db.relationship('User', foreign_keys=[follower_userid],
                                    backref='follower')
    following_user = db.relationship('User', foreign_keys=[following_userid],
                                     backref='follow')

    def __init__(self, follower_userid, following_userid):
        self.follower_userid = follower_userid
        self.following_userid = following_userid


class Post(db.Model):
    PUBLIC = 1
    PRIVATE = -1
    PROTECTED = 0
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_url = db.Column(db.String(1000))
    post_privacy = db.Column(db.Integer)
    puid = db.Column(db.Integer, db.ForeignKey('user.uid'))
    user = db.relationship('User',
                           backref=db.backref('post', lazy=True))
    created_time = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, image_url, post_privacy, puid):
        self.image_url = image_url
        self.puid = puid
        self.post_privacy = post_privacy


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.pid'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
    comment_text = db.Column(db.String(50))
    user = db.relationship('User',
                           backref=db.backref('comment', lazy=True))
    post = db.relationship('Post',
                           backref=db.backref('comment', lazy=True,
                                              cascade="all, delete-orphan"))

    def __init__(self, post_id, user_id, comment_text):
        self.post_id = post_id
        self.user_id = user_id
        self.comment_text = comment_text


class Like(db.Model):
    UN_LIKE = 0
    post_id = db.Column(db.Integer, db.ForeignKey('post.pid'),
                        primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'),
                        primary_key=True)
    user = db.relationship('User',
                           backref=db.backref('like', lazy=True))
    post = db.relationship('Post',
                           backref=db.backref('like', lazy=True,
                                              cascade="all, delete-orphan"))

    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id


db.create_all()
