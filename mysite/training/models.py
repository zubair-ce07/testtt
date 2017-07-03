# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as get_text

class Technology(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Assignment(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    completion_status = models.BooleanField(default=False)
    technology_used = models.ForeignKey(Technology)

    def __str__(self):
        return self.title


class Trainee(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(max_length=200,
                                upload_to="trainee_images/",
                                default="default.png")
    assignments = models.ManyToManyField(Assignment)

    def __str__(self):
        return self.name


class Trainer(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(max_length=200,
                                upload_to="trainer_images/",
                                default="default.png")
    assignments = models.ManyToManyField(Assignment)
    trainee = models.ForeignKey(Trainee)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser,
                     **extra_fields):
        now = timezone.now()

        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, is_staff=is_staff,
                          is_active=True, is_superuser=is_superuser,
                          last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True, unique=True)
    # country = models.CharField(max_length=30, blank=True)
    # is_staff = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=True)
    # is_superuser = models.BooleanField(default=False)
    # last_login = models. DateTimeField(default=timezone.now())
    # date_joined = models.DateTimeField(default=timezone.now())

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'email']

    objects = CustomUserManager()

    class Meta:
        verbose_name = get_text('user')
        verbose_name_plural = get_text('users')

    def get_full_name(self):
        full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
