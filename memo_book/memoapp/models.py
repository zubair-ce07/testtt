from django.db import models
from django.contrib.auth.models import User


class Memory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    url = models.CharField(max_length=300)
    tags = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')