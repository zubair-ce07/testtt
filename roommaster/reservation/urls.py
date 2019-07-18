from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='reservation-home'),
    path('home/', views.home, name='reservation-home'),
    path('rooms/', views.rooms, name='reservation-rooms'),
    path('customers/', views.customers, name='reservation-customers'),
    path('reservations/', views.reservations, name='reservation-reservations'),
    path('employees/', views.employees, name='reservation-employees'),
]
