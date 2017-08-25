from django.db import models
from backend.users.models import User
from backend.news.models import News
# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(User)
    news = models.ForeignKey(News)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return "{} | {} | {}".format(self.user, str(self.date), self.news)
