from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
     def create_user(self, **kwargs):
        email = kwargs['email']
        password = kwargs['password']
        first_name = kwargs['first_name']
        last_name = kwargs['last_name']
        date_of_birth = kwargs['date_of_birth']
        gender = kwargs['gender']
        if not any([email, password, first_name, last_name, date_of_birth, gender]):
            raise ValueError("Users must enter all the required fields! ")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender
        )
        user.set_password(password)
        user.save(using=self.db)
        return user


class User(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', 'gender']

    objects = UserManager()

    def __str__(self):
        return self.email

