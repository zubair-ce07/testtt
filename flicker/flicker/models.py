import datetime

from flask_sqlalchemy import SQLAlchemy
from flicker import app

db = SQLAlchemy(app)


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True, index=True)
    dateofreg = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(50), index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.pid'))

    def __init__(self, tag, post_id):
        self.tag = tag
        self.post_id = post_id


class Follow(db.Model):
    following_userid = db.Column(db.Integer, db.ForeignKey('user.uid'),
                                 primary_key=True)
    followed_userid = db.Column(db.Integer, db.ForeignKey('user.uid'),
                                primary_key=True)
    following_username = db.Column(db.String(50))
    followed_username = db.Column(db.String(50))

    def __init__(self, following_userid, followed_userid, following_username,
                 followed_username):
        self.following_userid = following_userid
        self.followed_userid = followed_userid
        self.following_username = following_username
        self.followed_username = followed_username


class Posts(db.Model):
    pid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_url = db.Column(db.String(1000))
    post_privacy = db.Column(db.Integer)
    puid = db.Column(db.Integer, db.ForeignKey('user.uid'))

    def __init__(self, image_url, post_privacy, puid):
        self.image_url = image_url
        self.puid = puid
        self.post_privacy = post_privacy


db.create_all()
