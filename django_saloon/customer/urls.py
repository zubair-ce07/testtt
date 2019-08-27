"""customer urls module."""
from django.urls import path

from .views import UserRegisterView, ProfileView, ReservationsListView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='customer_register'),
    path('profile/', ProfileView.as_view(), name='customer_profile'),
    path('myreservations/', ReservationsListView.as_view(),
         name='customer_reservations')
]
