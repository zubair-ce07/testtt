from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.forms import ModelForm
from datetime import date

class CustomUser(AbstractUser):
    """ class to add built in auth functionality. """
    phone = models.CharField(max_length=100, default='', \
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
    status = models.CharField(max_length=50, choices=status_type, default='Not Approved')


    def __str__(self):
        return self.username


class Product(models.Model):
    """ Field to save product info."""
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

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class Order(models.Model):
    """ Get user info for placing order. """
    id = models.AutoField(primary_key=True)
    products = models.CharField(max_length=5000)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=16)
    order_date = models.DateField(default=date.today())
    # order_items = models.ManyToManyField(Product, through='OrderItems', related_name=u'order_items')

    def __str__(self):
        return self.name


class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=64)
