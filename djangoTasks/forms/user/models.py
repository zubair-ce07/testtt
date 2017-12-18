"""Contain Model classes"""
import datetime

from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import extras
from django.shortcuts import reverse
from django.conf import settings


class MaleUsers(models.Manager):
    """custom user's model manager to filter male user"""
    def get_queryset(self):
        """
        filters male users
        :return: male user's object
        """
        return super(MaleUsers, self).get_queryset().filter(gender='m')


class FemaleUsers(models.Manager):
    """custom user's model manager to filter female user"""
    def get_queryset(self):
        """
        filters female users
        :return: female user's object
        """
        return super(FemaleUsers, self).get_queryset().filter(gender='f')


class LahoreCitizens(models.Manager):
    """custom user's model manager to filter user who lives in 'Lahore'"""
    def get_queryset(self):
        """
        filters user who lives in Lahore
        :return: citizen of Lahore user's object
        """
        return super(LahoreCitizens, self).get_queryset().filter(
            userprofile__city='Lahore'
        )


class MyUser(AbstractUser):
    """
    custom user's model to contain extra fields but extended from
    auth.user.
    """
    gender = models.CharField(max_length=8)
    objects = UserManager()

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'pk': self.pk})

    def get_url_for_authentication(self):
        return reverse('auth_no_password', kwargs={'username': self.username})

    def save(self, *args, **kwargs):
        """
        save user's model object and userprofile as well
        :param args: arguments
        :param kwargs: keyword arguments
        """
        profile_form = None
        if 'profile_form' in kwargs.keys():
            profile_form = kwargs.pop('profile_form')
        super(MyUser, self).save(*args, **kwargs)
        if profile_form:
            profile = profile_form.save(commit=False)
            profile.user = self
            profile.save()


class Product(models.Model):
    """Model Class for table prduct"""
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    price = models.IntegerField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="products"
    )

    def get_absolute_url(self):
        return reverse('view_product_detail', kwargs={'pk': self.pk})


class UserProfile(models.Model):
    """Model class for userprofile table"""
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    birthday = models.DateField()
    age_year = models.IntegerField(null=True, default=None)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def clean(self):
        """
        validation at model level, restrict user with age less than 18
        :raises Validation Error: if age is less than 18
        """
        today = datetime.date.today()
        birthday = self.birthday
        age_year = today.year - birthday.year
        if today.month < birthday.month or today.month == birthday.month and\
                today.day < birthday.day:
            age_year = age_year - 1

        if age_year < 18:
            raise ValidationError({'birthday': 'Age must be 18'})

    def save(self, **kwargs):
        """
        save 'userprofile' model and populate age field by calculating from
        birthday date.
        :param **kwargs: keyword arguments
        """
        today = datetime.date.today()
        birthday = self.birthday
        age_year = today.year - birthday.year
        if today.month < birthday.month or today.month == birthday.month \
                and today.day < birthday.day:
            age_year = age_year - 1
        self.age_year = age_year
        super(UserProfile, self).save()
