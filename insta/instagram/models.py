from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
# from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, )
    date_of_birth = models.DateField(blank=False, null=False)
    bio = models.TextField(max_length=300)
    # following =

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth', ]


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # name = models.CharField(max_length=50, null=False)
#     # email = models.EmailField(null=False)
#     # username = models.CharField(max_length=30, unique=True, null=False)
#     # password = models.CharField(max_length=50, null=False)
#     bio = models.TextField(max_length=300, blank=True)
#     following = models.ManyToManyField('self', blank=True, symmetrical=False)
#     # followed_by = models.ManyToManyField('self', blank=True, symmetrical=False)
#     # posts = models.ManyToManyField('Post', blank=True)
#
#     def __str__(self):
#         return self.user.username
#
#     class Meta:
#         ordering = ['user__username']
#
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class Post(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Like(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    like_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.like_timestamp)+' '+self.user.username


class Comment(models.Model):
    user = models.ForeignKey('Profile', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment_timestamp = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=150, null=False)

    def __str__(self):
        return self.text
