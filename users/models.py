""" It is model shows table structure of Order, products and users."""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


from datetime import date

class CustomUser(AbstractUser):
    """ class to add built in auth functionality. """
    phone = models.CharField(max_length=12, default='', \
        validators=[
            RegexValidator(
                regex='^[\d]{4}-[\d]{7}$',
                message=(u"Format should be 1234-1234567"),
                )
            ])
    address = models.CharField(max_length=100, default='')
    user_types = (
        ('Buyer', 'Buyer'),
        ('Manager', 'Manager'),
    )
    status_type = (
        ('Approved', 'Approved'),
        ('Not Approved', 'Not Approved'),
    )
    type = models.CharField(max_length=50, choices=user_types, default='buyer')
    role = models.CharField(max_length=50, choices=status_type, default='Not Approved')


    def __str__(self):
        return self.username


class Product(models.Model):
    """ Field to save product info."""
    category_types = (
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Kids', 'Kids'),
    )
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=10, choices=category_types)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    description = models.TextField(max_length=200)
    pub_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='users/images')

    def __str__(self):
        return self.name


class Order(models.Model):
    """ Fields for placing order. """

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=16)
    order_date = models.DateField(default=date.today())

    def __str__(self):
        return self.name


class OrderItems(models.Model):
    """ It contains relation of both order and product tables. """

    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='products')
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name='orders')
    quantity = models.IntegerField()
