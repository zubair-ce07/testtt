from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, email, date_of_birth, avatar, password=None,):
        if not email:
            raise ValueError('Users must have an email address')
        elif not username:
            raise ValueError('Users must have a username')
        elif not (first_name and last_name):
            raise ValueError('Users must have a first and last name')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            avatar=avatar
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, date_of_birth, avatar, password):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            avatar=avatar,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class FollowingManager(models.Manager):
    def get_queryset(self):
        return super(FollowingManager, self).get_queryset().values('following')


class FollowerManager(models.Manager):
    def get_queryset(self, followers_for):
        # return super(FollowerManager, self).get_queryset().filter(following__username=followers_for.username).all()
        return super(FollowerManager, self).get_queryset().filter(following__username=followers_for).all()
