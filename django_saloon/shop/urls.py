from django.urls import path
from django.contrib.auth import views as auth_views

from .views import Register, Profile, SaloonListView, MyShopListView, SaloonSlotListView

urlpatterns = [
    path('register/', Register.as_view(), name='shop_register'),
    path('profile/', Profile.as_view(), name='shop_profile'),
    path('saloons/', SaloonListView.as_view(), name='shop_list'),
    path('shop/<str:shop_name>', SaloonSlotListView.as_view(), name='shop_slots'),
    path('mysaloon/', MyShopListView.as_view(), name='my_shop')
]
