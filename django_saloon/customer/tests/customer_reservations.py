"""customer test module."""
from datetime import datetime

from django.urls import reverse
from rest_framework import status

from shop.models import Reservation
from core.tests import utils


class TestCustomerReservation(utils.Customer_Mixin_Test_Case):
    """customer reservation test class."""

    def setUp(self):
        """creating customer,saloon,timeslot and reservation for
        user reservation test case."""
        self.url = reverse('api_customer_reservations')
        super(TestCustomerReservation, self).setUp()
        self.client.force_authenticate(user=self.user)

        self.username = 'rose'
        self.email = 'rose@gmail.com'
        self.password = 'rose'

        self.saloon_user = utils.create_shop_user_instance(
            self.username, self.email, self.password)

        self.time_slot = utils.create_time_slot_instance(
            self.saloon_user.saloon, datetime.now())

        self.reservation = utils.create_reservation_instance(
            self.time_slot, self.user.customer)

    def test_customer_reservations_sucessful(self):
        """testing api customer list reservations."""
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Reservation.objects.get(
            customer=self.user.customer), self.reservation)
