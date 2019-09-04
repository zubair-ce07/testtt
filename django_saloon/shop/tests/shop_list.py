from django.urls import reverse
from rest_framework import status

from core.tests import utils
# from shop.models import Saloon


class TestShopList(utils.Shop_Mixin_Test_Case):

    def setUp(self):
        """creating saloons shop list test case."""
        self.url = reverse('api_shop_list')
        super(TestShopList, self).setUp()
        self.client.force_authenticate(user=self.user)

    def test_shop_list(self):
        """Customer failed update test providing username that already exists."""
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data, Saloon.objects.all())
