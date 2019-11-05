from django.core.management.base import BaseCommand
from users.models import Product

def add_products():
    if not Product.objects.all():
        Product.objects.bulk_create([
            Product(name='Product 1', category='Kids', price=200, \
                image='users/images/download.jpeg', pub_date='2019-10-23'),
            Product(name='Product 2', category='Men', price=200, \
                image='users/images/download.jpeg', pub_date='2019-10-23'),
            Product(name='Product 3', category='Women', price=200, \
                image='users/images/download.jpeg', pub_date='2019-10-23')])

class Command(BaseCommand):
    """ Main class which extends base command method. """

    def handle(self, **options):
        """ Function to execute when command run. """
        add_products()
