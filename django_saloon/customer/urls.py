"""customer urls module."""
from django.urls import path

from customer.views import ProfileView, ReservationsListView, \
    CustomerUpdateApiView, MyReservationsApiView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='customer_profile'),
    path('api/profile/', CustomerUpdateApiView.as_view(),
         name='api_customer_profile'),
    path('myreservations/', ReservationsListView.as_view(),
         name='customer_reservations'),
    path('api/myreservations/', MyReservationsApiView.as_view(),
         name='api_customer_reservations'),
]
