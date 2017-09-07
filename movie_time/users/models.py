import os
import time
from uuid import uuid4
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token


class UserManager(BaseUserManager):
    """
    Provides a manager to create user objects and super user
    """
    def create_user(self, email, password, date_of_birth=None, first_name=None, last_name=None, photo=None):
        """
        Save user object created with given parameters to database and returns user

        Arguments:
            email (str): email address
            password (str): password to be set
            date_of_birth (Date): date of birth
            first_name (str): first name of user
            last_name (str): last name of user
            photo (str): profile image for the user

        Returns:
             user (CustomUser): user created with given attributes
        """
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            photo=photo
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff_user(self, email, password, is_admin=False, is_moderator=False):
        """
        Creates user as admin for staff privileges

        Arguments:
            email (str): email address
            password (str): password to be set
            is_admin (Boolean): does user have admin privileges
            is_moderator (Boolean): does user have moderator privileges

        Returns:
            user (CustomUser): user created with given attributes
        """
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_admin = is_admin
        user.is_moderator = is_moderator
        user.save(using=self._db)
        return user


def image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join('uploads/{}'.format(time.strftime("%Y/%m/")), filename)


class User(AbstractBaseUser):
    """
    Custom User model class to store users
    """
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True, upload_to=image_path)
    is_admin = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    follows = models.ManyToManyField('User', symmetrical=False, related_name='followed_by')

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(instance=None, created=False, **kwargs):
    """
    if a new user is created then create a new token for that user
    Arguments:
         instance (User): Newly created user instance
         created (bool): weather user is newly created or just saved
    """
    if created:
        Token.objects.create(user=instance)


class FollowRequest(models.Model):
    NEW = 1
    ACCEPTED = 2
    BLOCKED = 3

    STATUSES = (
        (NEW, 'New'),
        (ACCEPTED, 'Accepted'),
        (BLOCKED, 'Blocked')
    )

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    status = models.PositiveSmallIntegerField(choices=STATUSES)


@receiver(post_save, sender=FollowRequest)
def create_auth_token(instance=None, created=False, **kwargs):
    """
    if a new request is created then create a notification for that target user
    Arguments:
         instance (FollowRequest): Newly created request instance
         created (bool): weather request is newly created or just saved
    """
    if created:
        Notification.objects.create(
            recipient=instance.to_user,
            actor=instance.from_user,
            verb=Notification.FOLL0W_REQUEST,
            action_object=instance
        )


class Notification(models.Model):
    MOVIE_RELEASED = 1
    FOLL0W_REQUEST = 2
    ACTIONS = (
        (MOVIE_RELEASED, 'Movie Released'),
        (FOLL0W_REQUEST, 'Follow Request')
    )
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    verb = models.PositiveSmallIntegerField(choices=ACTIONS)
    timestamp = models.DateTimeField(default=timezone.now)
    deleted = models.BooleanField(default=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    action_object = GenericForeignKey()
