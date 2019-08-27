from django.urls import path
from django.contrib.auth import views as auth_views

from .views import UserRegisterView, ProfileView, SaloonListView, MyShopListView, SaloonSlotListView, ReservationsListView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='shop_register'),
    path('profile/', ProfileView.as_view(), name='shop_profile'),
    path('saloons/', SaloonListView.as_view(), name='shop_list'),
    path('shop/<str:shop_name>', SaloonSlotListView.as_view(), name='shop_slots'),
    path('mysaloon/', MyShopListView.as_view(), name='my_shop'),
    path('myreservations/', ReservationsListView.as_view(), name='shop_reservations')
]
