from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class CustomUserManager(BaseUserManager):
    """
    Provides a manager to create user objects and super user
    """
    def create_user(self, email, password, first_name=None, last_name=None):
        """
        Save user object created with given parameters to database and returns user

        Arguments:
            email (str): email address
            password (str): password to be set
            first_name (str): first name of user
            last_name (str): last name of user
        Returns:
             user (User): user created with given attributes
        """
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates user as admin for staff privileges

        Arguments:
            email (str): email address
            password (str): password to be set
        Returns:
            user (User): user created with given attributes
        """
        user = self.create_user(
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Model to store user's details
    """
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def get_short_name(self):
        return self.last_name

    def get_full_name(self):
        return self.first_name


class Designation(models.Model):
    """
    Model class to store job titles as designations
    """
    job_title = models.CharField(max_length=30, unique=True)

    @classmethod
    def get_or_create(cls, job_title):
        """
        Checks if job title is already in database
        if not saves it and returns designation with job title

        Arguments:
            job_title (str): job title against which to search
        Returns:
            designation (Designation): designation with provided job title
        """
        designations = cls.objects.filter(job_title=job_title)

        if not designations.exists():
            designation = cls.objects.create(job_title=job_title)
        else:
            designation = designations.first()

        return designation


class Address(models.Model):
    """
    model to store address which consists of street address and city
    """
    street = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)


class Profile(models.Model):
    """
    model to store additional data about user
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=30)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation)


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
