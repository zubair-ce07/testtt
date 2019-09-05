"""list saloon test file."""
from rest_framework import status
from django.urls import reverse

from core.tests import utils
from shop.models import TimeSlot
from shop.serializers import TimeSlotSerializerForCustomers


class TestSaloonSlotsList(utils.Shop_Mixin_Test_Case):
    """list saloon test class."""

    def setUp(self):
        """creating saloons shop list test case."""
        self.url_name = 'api_shop_slots'
        super(TestSaloonSlotsList, self).setUp()
        self.client.force_authenticate(user=self.customer_user)

    def test_shop_list(self):
        """Shop List failed update test providing username that already exists."""
        url = reverse(self.url_name, args=['rose saloon'])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, create_response_data('rose saloon'))

    def test_shop_list_with_wrong_shop_name(self):
        """Shop List failed update test providing username that already exists."""
        url = reverse(self.url_name, args=['abcd'])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


def create_response_data(shop_name):
    """creating response data"""
    response_query_set = TimeSlot.objects.filter(
        saloon__shop_name=shop_name)
    serializer = TimeSlotSerializerForCustomers(response_query_set, many=True)
    return serializer.data
