from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, address, gender, born_on, password=None):
        user = self.model(email=UserManager.normalize_email(email), first_name=first_name,
                          last_name=last_name, address=address, gender=gender, born_on=born_on)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, address, gender, born_on, password):
        user = self.create_user(email=email, first_name=first_name, last_name=last_name,
                                address=address, gender=gender, born_on=born_on, password=password)
        user.is_admin = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.OneToOneField('Address')
    gender = models.CharField(max_length=100)

    born_on = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'address', 'gender', 'dob']

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_short_name(self):
        """ The user is identified by their email address """
        return self.first_name

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    # noinspection PyMethodMayBeStatic
    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?
           Simplest possible answer: Yes, always"""
        return True

    # noinspection PyMethodMayBeStatic
    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?
           Simplest possible answer: Yes, always"""
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?
           Simplest possible answer: All admins are staff"""
        return self.is_admin


class Address(models.Model):
    zip_code = models.CharField(max_length=50)
    street = models.CharField(max_length=255)
    route = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)





