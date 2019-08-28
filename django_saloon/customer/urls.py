"""customer urls module."""
from django.urls import path

from .views import ProfileView, ReservationsListView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='customer_profile'),
    path('myreservations/', ReservationsListView.as_view(),
         name='customer_reservations')
]
