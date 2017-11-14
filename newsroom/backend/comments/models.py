from django.db import models
from backend.users.models import User
from backend.news.models import News
# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(User)
    news = models.ForeignKey(News)
    parent = models.ForeignKey('Comment', null=True, blank=True, related_name='replies')
    post_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        return "{} | {} | {}".format(self.user, str(self.post_date), self.news)

