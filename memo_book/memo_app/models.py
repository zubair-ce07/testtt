from django.db import models
from django.contrib.auth.models import User

class Memory(models.Model):
    user_id = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    text = models.TextField()
    url = models.CharField(max_length=300)
    tags = models.CharField(max_length=200)
    image = models.FileField()