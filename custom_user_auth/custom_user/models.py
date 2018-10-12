"""
this module contains all the modles of this django app
"""
from datetime import datetime
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, Permission, Group
from . import strings

class MyUserManager(BaseUserManager):
    """
    a user manager for custom user
    """
    def create_user(self, username, password):
        """
        a method that create a user with provided username and password
        :param username:
        :param password:
        :return:
        """
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            username=(username),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        a method that create a super user with provided username and password
        :param username:
        :param password:
        :return:
        """
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            username=(username),
        )

        user.set_password(password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    """
    a custom user codel class
    """
    username = models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            'unique': strings.USERNAME_UNIQUE,
            'required': strings.USERNAME_REQUIRED,
            'max_length': strings.USERNAME_MAX_LENGTH,
        },
    )

    first_name = models.CharField(
        max_length=40,
        verbose_name="first name",
        blank=True,
        error_messages={
            'max_length': strings.FIRSTNAME_MAX_LENGTH,
        },
    )

    last_name = models.CharField(
        max_length=40,
        verbose_name="last name",
        blank=True,
        error_messages={
            'max_length': strings.LASTNAME_MAX_LENGTH,
        },
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        blank=True,
        error_messages={
            'max_length': strings.EMAIL_MAX_LENGTH,
        },
    )

    is_active = models.BooleanField(verbose_name='active', default=True)
    is_superuser = models.BooleanField(verbose_name='superuser status', default=False)
    is_staff = models.BooleanField(verbose_name='staff status', default=True)

    date_joined = models.DateTimeField(default=str(datetime.now()))
    permissions = models.ManyToManyField(Permission, blank=True)
    groups = models.ManyToManyField(Group, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    # REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?
        # Simplest possible answer: Yes, always"""
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?
        # Simplest possible answer: Yes, always"""
        return True



    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    class Meta:
        """
        Meta class of custom user
        """
        verbose_name = "user"
