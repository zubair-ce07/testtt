"""Delete reservation test file."""
from django.urls import reverse
from rest_framework import status

from core.tests import utils


class TestDeleteReservation(utils.Shop_Mixin_Test_Case):
    """Delete reservation class."""

    def setUp(self):
        """Create saloons delete reservation test case."""
        self.url_name = 'api_delete_slots'
        super(TestDeleteReservation, self).setUp()
        self.client.force_authenticate(user=self.user)

    def test_shop_delete_reservation_by_customer(self):
        """Shop delete reservation by customer."""
        self.client.force_authenticate(user=self.customer_user)
        url = reverse(self.url_name, args=['1'])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_shop_delete_reservation_by_saloon(self):
        """Shop delete reservation by saloon."""
        url = reverse(self.url_name, args=['1'])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_shop_delete_reservation_by_another_customer(self):
        """Shop delete reservation by another customer."""
        another_customer = utils.create_customer_user_instance(
            'abc', 'abc@gmail.com', 'abc')
        self.client.force_authenticate(user=another_customer)
        url = reverse(self.url_name, args=['1'])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_shop_delete_reservation_by_another_saloon(self):
        """Shop delete reservation by another saloon."""
        another_customer = utils.create_shop_user_instance(
            'abc', 'abc@gmail.com', 'abc')
        self.client.force_authenticate(user=another_customer)
        url = reverse(self.url_name, args=['1'])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_shop_delete_reservation_by_wrong_id(self):
        """Shop delete reservation by wrong id."""
        url = reverse(self.url_name, args=['122'])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
