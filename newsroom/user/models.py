from django.db import models
from django.contrib.auth.models import User
from news.models import Category


class UserInterest(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('category', 'user'), )

    def __str__(self):
        return '{user} | {category}'.format(user=self.user, category=self.category)
