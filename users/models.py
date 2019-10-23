from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.email


class Product(models.Model):
    """ Field to save product Info."""
    category_types = (
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Kids', 'Kids'),
    )
    id = models.AutoField
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=10, choices=category_types)
    price = models.IntegerField()
    description = models.CharField(max_length=200)
    pub_date = models.DateField()
    image = models.ImageField(upload_to='users/images')

    def __str__(self):
        return self.name
    objects = models.Manager()