""" Page to show what action to perform on given url. """

from django.urls import path
from .views import SignUpView, ProductsList, OrderProducts

urlpatterns = [
    path('', ProductsList.as_view(), name='home'),
    path('order/', OrderProducts.as_view(), name='order'),
]