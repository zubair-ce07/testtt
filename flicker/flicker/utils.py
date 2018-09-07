""" Contains helper function for views rendering """
import os
import random
import string

from flask import session
from sqlalchemy import and_, desc, or_

from .models import User, Post, Tag, Follow, Like, Comment, db


def collect_tag_posts(search_tag):
    """ Search Posts by Tags """
    following_users = db.session.query(Follow.following_userid).filter(
        Follow.follower_userid == session['current_user_id']).all()
    following_users = [user[0] for user in following_users]
    tagged_posts = Tag.query.filter(Tag.tag.like('%' + search_tag + '%'),
                                    Tag.post).with_entities(Post)
    tagged_posts = tagged_posts.filter(
        or_(Post.puid == session['current_user_id'],
            Post.post_privacy == Post.PUBLIC, (
                and_(Post.puid.in_(following_users),
                     Post.post_privacy != Post.PRIVATE)))).order_by(
        desc(Post.pid)).all()
    user_likes = db.session.query(Like.post_id).filter(
        Like.user_id == session['current_user_id']).all()
    return tagged_posts, user_likes


def collect_allowed_posts():
    """Collects Allowed Posts For
        Logged in User
    """
    public_posts = Post.query.filter(
        (Post.post_privacy == Post.PUBLIC) | (
                Post.puid == session['current_user_id'])
    ).order_by(desc(Post.pid)).all()
    following_users = db.session.query(Follow.following_userid).filter(
        Follow.follower_userid == session['current_user_id']).all()
    following_users = [user[0] for user in following_users]
    following_users_posts = Post.query.filter(
        Post.puid.in_(following_users))
    following_users_posts = following_users_posts.filter(
        Post.post_privacy == Post.PROTECTED).order_by(desc(Post.pid)).all()
    public_posts.extend(following_users_posts)
    user_likes = db.session.query(Like.post_id).filter(
        Like.user_id == session['current_user_id']).all()
    return public_posts, user_likes


def add_post_comment(post_id, comment_text):
    """ Insert Logged In User Comment """
    comment = Comment(post_id, session['current_user_id'], comment_text)
    db.session.add(comment)
    db.session.commit()


def update_post_like_status(post_id, like_status):
    """ Update logged In User Likes """
    if int(like_status) == Like.UN_LIKE:
        like = Like(post_id, session['current_user_id'])
        db.session.add(like)
        db.session.commit()
    else:
        user_like = Like.query.filter(
            Like.post_id == post_id, Like.user_id ==
            session['current_user_id']).first()
        db.session.delete(user_like)
        db.session.commit()


def delete_user_comment(comment_id):
    """ Delete Logged In User Comment """
    comment = Comment.query.filter(
        Comment.comment_id == comment_id).first()
    db.session.delete(comment)
    db.session.commit()


def allowed_file(filename):
    """Checks Allowed Extension for Profile Pic / Post Pic"""
    allowed_extensions = set(['png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def generate_random_string():
    """ Generates Random String """
    size = 7
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(size))


def append_random_string(filename):
    """Appends Random String to Filename"""
    name, ext = os.path.splitext(filename)
    return "{name}_{uid}{ext}".format(name=name, uid=generate_random_string(),
                                      ext=ext)


def save_post_tags(tags_list, post_id):
    """ Save new Post's Tag"""
    tags_list = tags_list.split(" ")
    for tag in tags_list:
        tag_obj = Tag(tag, post_id)
        db.session.add(tag_obj)
        db.session.commit()


def update_follow_status(profile_user_id, follow_status):
    """  Updates Follow  Status of Users"""
    current_user_id = session['current_user_id']
    profile_user_id = int(profile_user_id)
    if int(follow_status) == Follow.Follow:
        follow_instance = db.session.query(Follow).filter(
            Follow.follower_userid == current_user_id,
            Follow.following_userid == profile_user_id).first()
        db.session.delete(follow_instance)
        db.session.commit()
    if int(follow_status) == Follow.Un_Follow:
        follow = Follow(current_user_id, profile_user_id)
        db.session.add(follow)
        db.session.commit()


def check_follow_status(profile_user_id):
    """ Check  Follow Status"""
    current_user_id = session['current_user_id']
    profile_user_id = int(profile_user_id)
    follow_status = db.session.query(Follow).filter(
        Follow.follower_userid == current_user_id,
        Follow.following_userid == profile_user_id).all()
    if follow_status:
        return True
    return False


def validate_user_email(user_email):
    """ Verify Unique Email of New User """
    user = User.query.filter_by(email=user_email).first()
    if user:
        return False
    return True


def validate_username(username):
    """ Verify Unique Username of New User """
    log_user_username = User.query.filter_by(username=username).first()
    if log_user_username:
        return False
    return True
