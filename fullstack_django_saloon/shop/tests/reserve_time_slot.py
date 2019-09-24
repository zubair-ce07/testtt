"""Reserve time slot test file."""
from datetime import datetime

from django.urls import reverse
from rest_framework import status

from core.tests import utils
from shop.models import Reservation


class TestReserveTimeSlot(utils.Shop_Mixin_Test_Case):
    """Reserve time slot test class."""

    def setUp(self):
        """Create saloons reserve time slot test cases."""
        self.url_name = 'api_reserve_slot'
        super(TestReserveTimeSlot, self).setUp()
        utils.create_time_slot_instance(
            self.user.saloon, datetime.now())
        self.client.force_authenticate(user=self.customer_user)

    def test_reserve_time_slot(self):
        """Reserve time slot by customer."""
        url = reverse(self.url_name)
        request_data = {
            'time_slot': 2
        }
        response = self.client.post(url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Reservation.objects.get(
            id=1).customer, self.customer_user.customer)

    def test_reserve_time_slot_by_shop(self):
        """Reserve time slot by shop."""
        self.client.force_authenticate(user=self.user)
        url = reverse(self.url_name)
        request_data = {
            'time_slot': 2
        }
        response = self.client.post(url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reserve_already_reserved_time_slot(self):
        """Reserve already reserved time slot."""
        url = reverse(self.url_name)
        request_data = {
            'time_slot': 1
        }
        response = self.client.post(url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reserve_time_slot_time_slot_id_not_provided(self):
        """Reserve time slot but time slot id not provided."""
        url = reverse(self.url_name)
        request_data = {
        }
        response = self.client.post(url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
