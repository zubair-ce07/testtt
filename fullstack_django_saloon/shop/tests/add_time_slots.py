"""Test case file for add slot."""
from django.urls import reverse
from rest_framework import status

from core.tests import utils
from shop.models import TimeSlot


class TestAddTimeSlots(utils.Shop_Mixin_Test_Case):
    """Shop update test class."""

    def setUp(self):
        """Create customer,saloon,timeslot and reservation."""
        self.url = reverse('api_my_shop')

        super(TestAddTimeSlots, self).setUp()
        self.client.force_authenticate(user=self.user)

    def test_add_time_slots_(self):
        """Shop sucessful add time slots test."""
        request_data = {
            'start_date': '2019-08-26',
            'end_date': '2019-08-27',
            'start_time': '10',
            'number_of_slots': '10',
            'slot_duration': '45'
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TimeSlot.objects.filter(
            saloon=self.user.saloon).count(), 21)

    def test_add_time_slots_by_customer_user(self):
        """Shop failed add time slots by customer user test."""
        request_data = {
            'start_date': '2019-08-26',
            'end_date': '2019-08-27',
            'start_time': '10',
            'number_of_slots': '10',
            'slot_duration': '45'
        }
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_time_slots_wrong_start_end_dates(self):
        """Shop failed add time slots where start date is greater then end date test."""
        request_data = {
            'start_date': '2019-08-27',
            'end_date': '2019-08-26',
            'start_time': '10',
            'number_of_slots': '10',
            'slot_duration': '45'
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_time_slots_dates_not_provided(self):
        """Shop failed add time slots when dates are not provided."""
        request_data = {
            'start_time': '10',
            'number_of_slots': '10',
            'slot_duration': '45'
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_time_slots_start_time_not_provided(self):
        """Shop failed add time slots when start time is not provided."""
        request_data = {
            'start_date': '2019-08-26',
            'end_date': '2019-08-27',
            'number_of_slots': '10',
            'slot_duration': '45'
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_time_slots_number_of_slots_not_provided(self):
        """Shop failed add time slots when number of slots are not provided."""
        request_data = {
            'start_date': '2019-08-26',
            'end_date': '2019-08-27',
            'start_time': '10',
            'slot_duration': '45'
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_time_slots_slot_duration_not_provided(self):
        """Shop failed add time slots when slot duaration is not provided."""
        request_data = {
            'start_date': '2019-08-27',
            'end_date': '2019-08-26',
            'start_time': '10',
            'number_of_slots': '10'
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_time_slots_slot_date_format_not_correct(self):
        """Shop failed add time slots when date format is not correct."""
        request_data = {
            'start_date': '2019-08',
            'end_date': '2019-08',
            'start_time': '10',
            'number_of_slots': '10'
        }
        response = self.client.post(self.url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
