from django.core.management.base import BaseCommand
from blog.models import User, Post, Category, Comment, Like_comment, Like_post
from datetime import datetime

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _populate_data(self):
        a_record = User(id=2, username="test_user_1", password='abc123456')
        a_record.save()

        a_record = User(id=3, username="test_user_2", password='abc123456')
        a_record.save()

        a_record = Category(id=1, category='politics')
        a_record.save()

        a_record = Category(id=2, category='sports')
        a_record.save()

        a_record = Post(id=1, title="post_1", modified_at=datetime.now(), body='curvy', author_id=1, category_id=1)
        a_record.save()

        a_record = Post(id=2, title="post_2", modified_at=datetime.now(), body='body_2', author_id=2, category_id=2)
        a_record.save()

        a_record = Comment(id=1, post_id=1, body='comment_1', user_id=3, created_at=datetime.now())
        a_record.save()

        a_record = Comment(id=2, post_id=1, body='comment_2', user_id=3, created_at=datetime.now())
        a_record.save()

        a_record = Comment(id=3, post_id=2, body='comment_3', user_id=3, created_at=datetime.now())
        a_record.save()

        a_record = Like_comment(comment_id=1, user_id=3, vote=1, created_at=datetime.now())
        a_record.save()

        a_record = Like_comment(comment_id=1, user_id=3, vote=1, created_at=datetime.now())
        a_record.save()

        a_record = Like_comment(comment_id=1, user_id=3, vote=-1, created_at=datetime.now())
        a_record.save()

        a_record = Like_comment(comment_id=2, user_id=3, vote=1, created_at=datetime.now())
        a_record.save()

        a_record = Like_comment(comment_id=3, user_id=3, vote=-1, created_at=datetime.now())
        a_record.save()

        a_record = Like_post(post_id=1, user_id=3, vote=1, created_at=datetime.now())
        a_record.save()

        a_record = Like_post(post_id=1, user_id=3, vote=1, created_at=datetime.now())
        a_record.save()

        a_record = Like_post(post_id=2, user_id=3, vote=-1, created_at=datetime.now())
        a_record.save()

    def handle(self, *args, **options):
        self._populate_data()
