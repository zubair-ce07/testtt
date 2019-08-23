from django.urls import path
from django.contrib.auth import views as auth_views

from .views import Register, Profile, SaloonListView, MyShopListView

urlpatterns = [
    path('register/', Register.as_view(), name='shop_register'),
    path('profile/', Profile.as_view(), name='shop_profile'),
    path('saloons/', SaloonListView.as_view(), name='shop_list'),
    path('mysaloon/', MyShopListView.as_view(), name='my_shop')
]
