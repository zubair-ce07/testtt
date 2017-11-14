from django.contrib.auth.models import User
from django.db import models

from backend.categories.models import Category

from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save


class UserInterest(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('category', 'user'), )

    def __str__(self):
        return '{user} | {category}'.format(user=self.user, category=self.category)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

