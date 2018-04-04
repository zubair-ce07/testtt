from django.core.management.base import BaseCommand
from blog.models import User, Post, Category, Comment, LikeComment, LikePost
from datetime import datetime

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _populate_data(self):
        md = User(username="Md", password='abc123456')
        md.save()

        hamza = User(username="hamza", password='abc123456')
        hamza.save()

        politics = Category(category='politics')
        politics.save()

        sports = Category(category='sports')
        sports.save()

        politics_post = Post(title="Pakistani_politics", modified_at=datetime.now(),
                             body='corrupt', author=hamza, category=politics)
        politics_post.save()

        sports_post = Post(title="e-sports", modified_at=datetime.now(), body='dota', author=md, category=sports)
        sports_post.save()

        comment_1 = Comment(post=sports_post, body='comment_1', user=md, created_at=datetime.now())
        comment_1.save()

        comment_2 = Comment(post=sports_post, body='comment_2', user=md, created_at=datetime.now())
        comment_2.save()

        comment_3 = Comment(post=politics_post, body='comment_3', user=md, created_at=datetime.now())
        comment_3.save()

        a_record = LikeComment(comment=comment_1, user=md, vote=1, created_at=datetime.now())
        a_record.save()

        a_record = LikeComment(comment=comment_1, user=md, vote=1, created_at=datetime.now())
        a_record.save()

        a_record = LikeComment(comment=comment_1, user=hamza, vote=-1, created_at=datetime.now())
        a_record.save()

        a_record = LikeComment(comment=comment_2, user=md, vote=1, created_at=datetime.now())
        a_record.save()

        a_record = LikeComment(comment=comment_3, user=hamza, vote=-1, created_at=datetime.now())
        a_record.save()

        a_record = LikePost(post=politics_post, user=md, vote=1, created_at=datetime.now())
        a_record.save()

        a_record = LikePost(post=politics_post, user=hamza, vote=1, created_at=datetime.now())
        a_record.save()

        a_record = LikePost(post=sports_post, user=md, vote=-1, created_at=datetime.now())
        a_record.save()

    def handle(self, *args, **options):
        self._populate_data()
