"""shop url module"""
from django.urls import path

from .views import (ProfileView, SaloonListView, MyShopListView,
                    SaloonSlotListView, ReservationsListView)

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='shop_profile'),
    path('saloons/', SaloonListView.as_view(), name='shop_list'),
    path('shop/<str:shop_name>', SaloonSlotListView.as_view(),
         name='shop_slots'),
    path('mysaloon/', MyShopListView.as_view(), name='my_shop'),
    path('myreservations/', ReservationsListView.as_view(),
         name='shop_reservations')
]
