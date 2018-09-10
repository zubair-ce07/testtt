from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, Permission, Group
from datetime import datetime


class MyUserManager(BaseUserManager):
    def create_user(self, username, password):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            username=(username),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            username=(username),
        )

        user.set_password(password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )

    first_name = models.CharField(
        max_length=40,
        verbose_name="first name",
        blank=True
    )

    last_name = models.CharField(
        max_length=40,
        verbose_name="last name",
        blank=True
    )

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        blank = True
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=str(datetime.now()))
    permissions = models.ManyToManyField(Permission)
    groups = models.ManyToManyField(Group)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    # REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
