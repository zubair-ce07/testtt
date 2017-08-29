from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class CustomUserManager(BaseUserManager):
    """
    Provides a manager to create user objects and super user
    """
    def create_user(self, email, password, phone=None):
        """
        Save user object created with given parameters to database and returns user

        Arguments:
            email (str): email address
            password (str): password to be set
            phone (str): phone no of user

        Returns:
             user (User): user created with given attributes
        """
        user = self.model(
            email=self.normalize_email(email),
            phone=phone
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
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, unique=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def get_short_name(self):
        return self.profile.first_name if self.profile else None

    def get_full_name(self):
        if self.profile:
            full_name = '{first} {last}'.format(first=self.profile.first_name, last=self.profile.last_name)
        else:
            full_name = None
        return full_name


class Designation(models.Model):
    """
    Model class to store job titles as designations
    """
    CHIEF_EXECUTIVE_OFFICER = 'CEO'
    SOFTWARE_ENGINEER = 'SE'
    SENIOR_SOFTWARE_ENGINEER = 'SSE'
    CHIEF_TECHNOLOGY_OFFICER = 'CTO'

    JOB_TITLES = (
        (CHIEF_EXECUTIVE_OFFICER, 'Chief Executive Officer'),
        (SOFTWARE_ENGINEER, 'Software Engineer'),
        (SENIOR_SOFTWARE_ENGINEER, 'Senior Software Engineer'),
        (CHIEF_TECHNOLOGY_OFFICER, 'Chief Technology Officer'),
    )

    job_title = models.CharField(max_length=30, choices=JOB_TITLES, unique=True)


class Address(models.Model):
    """
    model to store address which consists of street address and city
    """
    street = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    zip_code = models.PositiveSmallIntegerField(blank=True, null=True)


class Profile(models.Model):
    """
    model to store additional data about user
    """
    MALE = 'male'
    FEMALE = 'female'

    GENDERS = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=30, choices=GENDERS)
    address = models.OneToOneField(Address)
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


@receiver(post_delete, sender=Profile)
def auto_delete_address(sender, instance, **kwargs):
    instance.address.delete()
