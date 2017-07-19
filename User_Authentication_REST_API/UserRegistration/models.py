from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Create a new user with given parameters and return the user

        Args:
            email (str): The unique email given by the user
            password (str): Password consisting of 9 words not all numeric
            is_staff (boolean): Parameter to determine whether the user should be staff member or not
            is_superuser (boolean): Parameter to determine whether the user should be superuser or not
            extra_fields (extra parameters): Variable length arguments list for user fields

        Returns:
            CustomUser: The Created user
        """
        if not email:
            raise ValueError("Email Required")
        email = self.normalize_email(email)
        user = self.model(email=email, is_active=True, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """
        Calls private _create_user() method with given parameters to return user

        Args:
            email (str): The unique email given by the user
            password (str): Password consisting of 9 words not all numeric
            extra_fields (extra parameters): Variable length arguments list for user fields

        Returns:
            CustomUser: The user created after calling _create_user()
        """
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Calls private _create_user() method with given parameters to return superuser

        Args:
            email (str): The unique email given by the user
            password (str): Password consisting of 9 words not all numeric
            extra_fields (extra parameters): Variable length arguments list for user fields

        Returns:
            CustomUser: The user created after calling _create_user()
        """
        return self._create_user(email, password, True, True, **extra_fields)


class CustomUser(AbstractBaseUser):
    """
    Model for representing users

    Attributes:
        username (str): Username field of the user
        first_name (str): First name of the user
        last_name (str): Last name of the user
        email (email field): Uniques identifier for the users
        city (str): City where the user belongs
        profile_picture (ImageField): The display picture of the user
        height_field (int): Store the height of the profile picture uploaded. Default to 0
        width_field (int): Store the width of the profile picture uploaded. Default to 0
        is_active (boolean): Field to keep the check whether the user is active or not. Defaults to True
        is_superuser (boolean): Field to keep the check whether the user is superuser or not. Defaults to True
        is_staff (boolean): Field to keep the check whether the user is staff member or not. Defaults to True
    """
    username = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile_picture', blank=True, default='default.png',
                                        width_field="width_field", height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Return the full name for this User
        """
        full_name = "{} {}".format(self.first_name, self.last_name)
        return full_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_short_name(self):
        return self.first_name


class Task(models.Model):
    """
    Model to represent the tasks assigned to the users

    Attributes:
        user (CustomUser): Custom user object to which the tasks are assigned
        name (str): The unique name of the task acting as an identifier
        due_date (DateField): The due date for the task
        status (Boolean): The field representing the status of the task (complete or incomplete)
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True)
    due_date = models.DateField()
    status = models.BooleanField(default=False)

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """Creates Token for each new user created"""
    if created:
        Token.objects.create(user=instance)
