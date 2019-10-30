from django.core.management.base import BaseCommand
from users.models import Product

def add_dummy_data():
    if not Product.objects.all():
        for product in range(3):
            name = "Dummy Product"+ str(product)
            category = "Men"
            description = "Dummy Description"
            price = 240
            pub_date =  "2019-10-23"
            image = "users/images/kids.png"
            product = Product(name=name, category=category, description=description,
                              price=price, pub_date=pub_date, image=image)
            product.save()

class Command(BaseCommand):
    def handle(self, **options):
        add_dummy_data()
