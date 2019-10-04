from django.test import TestCase
from shopcity.models import Product


class AnimalTestCase(TestCase):
    def setUp(self):
        Product.objects.create(
            retailer_sku="lion-12345",
            name="roar",
            brand="NOVA",
            currency='GBP',
            price=1000,
            description='jugyufvjhvjhv',
            url='https://www.django-rest-framework.org/api-guide/testing/#api-test-cases',
            gender='men',
            out_of_stock=False,
        )

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Product.objects.get(retailer_sku="lion-12345")
        self.assertEqual(lion.name, "roar")

