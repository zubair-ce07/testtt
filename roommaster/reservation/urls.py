from django.urls import path, include
from django.contrib.auth import views as auth_views
from reservation.views import HomeView, RoomsView, CustomersView, ReservationsView, ReportView, RegistrationView
from reservation.views import EmployeesView, AvailabilityView, ReserveRoomView, AddReservation

urlpatterns = [
    path('', HomeView.as_view(), name='reservation-home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('home/', HomeView.as_view(), name='reservation-home'),
    path('rooms/', RoomsView.as_view(), name='reservation-rooms'),
    path('report/<int:id>/<str:checkin>/<str:checkout>', ReserveRoomView.as_view(), name='reservation-reserveroom'),
    path('employees/', EmployeesView.as_view(), name='reservation-employees'),
    path('customers/', CustomersView.as_view(), name='reservation-customers'),
    path('availability/', AvailabilityView.as_view(), name='reservation-availability'),
    path('reservations/', ReservationsView.as_view(), name='reservation-reservations'),
    path('addreservation/', AddReservation.as_view(), name='reservation-addreservation'),
    path('report/', ReportView.as_view(), name='reservation-report'),
    path('register/', RegistrationView.as_view(), name="reservation-register"),
    path('login/', auth_views.LoginView.as_view(template_name='reservation/login.html'), name='reservation-login'),
    path('logout/', auth_views.LogoutView.as_view(), name='reservation-logout')
]
