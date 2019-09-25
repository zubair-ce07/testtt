from django.db import models

# Create your models here.


def images_path():
    return "profile_pictures"


class User(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to=images_path)

    def __str__(self):
        return self.username
