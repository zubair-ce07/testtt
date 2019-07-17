from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='reservation-home'),
    path('home/', views.home, name='reservation-home'),
    path('rooms/', views.rooms, name='reservation-room'),
]
