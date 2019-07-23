from django.urls import path
from reservation.views import HomeView, RoomsView, CustomersView, ReservationsView, EmployeesView, AvailabilityView

urlpatterns = [
    path('', HomeView.as_view(), name='reservation-home'),
    path('home/', HomeView.as_view(), name='reservation-home'),
    path('rooms/', RoomsView.as_view(), name='reservation-rooms'),
    path('employees/', EmployeesView.as_view(), name='reservation-employees'),
    path('customers/', CustomersView.as_view(), name='reservation-customers'),
    path('availability/', AvailabilityView.as_view(), name='reservation-availability'),
    path('reservations/', ReservationsView.as_view(), name='reservation-reservations')
]
