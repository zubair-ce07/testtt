from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

GENDER_MAP = (
        ('M', 'MALE'),
        ('F', 'FEMALE'),
        ('U', 'UNISEX'),
        ('K', 'KIDS')
    )


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


class Brand(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=600)
    gender = models.CharField(max_length=4, choices=GENDER_MAP)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    url = models.URLField()


class ProductArticle(models.Model):
    product = models.ForeignKey(Product, related_name='articles', on_delete=models.CASCADE)
    color = models.CharField(max_length=30)
    price = models.FloatField()
    size = models.CharField(max_length=15)

