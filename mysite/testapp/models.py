# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone
from polymorphic.models import PolymorphicModel


# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):
	USERNAME_FIELD = 'username'
	PASSWORD_FIELD = 'password'
	REQUIRED_FIELDS = ['email']

	username = models.CharField(max_length=30, unique=True)
	phone = models.CharField(max_length=15)
	address = models.CharField(max_length=100)
	email = models.CharField(max_length=30, unique=True)
	password = models.CharField(max_length=150,blank=False)
	token = models.CharField(max_length=100)

	date_joined = models.DateTimeField(default=timezone.now)
	is_active   = models.BooleanField(default=True)
	is_admin    = models.BooleanField(default=False)
	is_staff    = models.BooleanField(default=False)

	objects = UserManager()

	def __str__(self):
		return self.username

	def get_short_name(self):
		return self.username

	@classmethod
	def create_user(cls, username, password, email):
		user = User(username=username, password=password, email=email)
		user.set_password(user.password)
		user.save()
		return user




class Friend(models.Model):
	user = models.ForeignKey(User,related_name="users",related_query_name="user", on_delete=models.CASCADE)
	friend = models.ForeignKey(User,related_name="friends",related_query_name="friend", on_delete=models.CASCADE)

	class Meta:
	    unique_together = (('user', 'friend'),)

	def __str__(self):
		return self.friend.username


class Post(PolymorphicModel):
	caption = models.CharField(max_length=200)
	posted_at = models.DateTimeField(auto_now_add=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.id)

class Audio(Post):
	audio_file = models.FileField(upload_to="media/audios/")

class Video(Post):
	video_file = models.FileField(upload_to="media/videos/")

class Image(Post):
	image_file = models.FileField(upload_to="media/images/")

class Comment(models.Model):
	comment = models.CharField(max_length=200)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

class Like(models.Model):

	class Meta:
		unique_together = (('user', 'post'),)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

