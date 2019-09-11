"""Add review test class file."""
from datetime import datetime

from django.urls import reverse
from rest_framework import status

from core.tests import utils
from shop.models import Review


class TestAddReview(utils.Shop_Mixin_Test_Case):
    """Add review test class."""

    def setUp(self):
        """Create saloons for add review test cases."""
        self.url_name = 'api_add_review'
        super(TestAddReview, self).setUp()
        utils.create_time_slot_instance(
            self.user.saloon, datetime.now())
        self.client.force_authenticate(user=self.customer_user)

    def test_add_review(self):
        """Add review by customer."""
        url = reverse(self.url_name)
        request_data = {
            'reservation': 1,
            'comment': 'sdasdas',
            'rating': 9
        }
        response = self.client.post(url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.get(
            reservation_id=1).reservation.customer, self.customer_user.customer)

    def test_add_review_wihtout_comment(self):
        """Add review by customer without comment."""
        url = reverse(self.url_name)
        request_data = {
            'reservation': 1,
            'rating': 9
        }
        response = self.client.post(url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.get(
            reservation_id=1).reservation.customer, self.customer_user.customer)

    def test_add_review_by_shop(self):
        """Add review by shop."""
        self.client.force_authenticate(user=self.user)
        url = reverse(self.url_name)
        request_data = {
            'reservation': 1,
            'comment': 'sdasdas',
            'rating': 9
        }
        response = self.client.post(url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_review_by_another_customer(self):
        """Add review by another customer."""
        another_customer = utils.create_customer_user_instance(
            'abc', 'acb@gmail.com', 'abc')
        self.client.force_authenticate(user=another_customer)
        url = reverse(self.url_name)
        request_data = {
            'reservation': 1,
            'comment': 'sdasdas',
            'rating': 9
        }
        response = self.client.post(url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_review_by_not_providing_reservation_id(self):
        """Add review by not providing reservation id."""
        url = reverse(self.url_name)
        request_data = {
            'comment': 'sdasdas',
            'rating': 9
        }
        response = self.client.post(url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_review_by_not_providing_rating(self):
        """Add review by not providing rating."""
        url = reverse(self.url_name)
        request_data = {
            'reservation': 1,
            'comment': 'sdasdas'
        }
        response = self.client.post(url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_review_of_already_reviewed_reservation(self):
        """Add review of already reviewed reservation."""
        url = reverse(self.url_name)
        request_data = {
            'reservation': 1,
            'comment': 'sdasdas',
            'rating': 9
        }
        review = Review(reservation=self.reservation,
                        comment='asdasd', rating=8)
        review.save()
        response = self.client.post(url, request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
