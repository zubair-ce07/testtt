"""shop url module"""
from django.urls import path

from shop.views import (ProfileView, SaloonListView, MyShopListView,
                        SaloonSlotListView, ReservationsListView, ApiShopList,
                        ApiShopUpdate, ApiListAddTimeSlots, ApiListSaloonSlots,
                        ApiDeleteReservation, ApiShopReservations,
                        ApiReserveTimeSlot
                        )

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='shop_profile'),
    path('api/profile/', ApiShopUpdate.as_view(),
         name='api_shop_profile'),
    path('saloons/', SaloonListView.as_view(), name='shop_list'),
    path('api/saloons/', ApiShopList.as_view(), name='api_shop_list'),
    path('shop/<str:shop_name>', SaloonSlotListView.as_view(),
         name='shop_slots'),
    path('api/shop/<str:shop_name>', ApiListSaloonSlots.as_view(),
         name='api_shop_slots'),
    path('api/cancel-reservation/<int:pk>', ApiDeleteReservation.as_view(),
         name='api_delete_slots'),
    path('mysaloon/', MyShopListView.as_view(), name='my_shop'),
    path('api/mysaloon/', ApiListAddTimeSlots.as_view(), name='api_my_shop'),
    path('myreservations/', ReservationsListView.as_view(),
         name='shop_reservations'),
    path('api/myreservations/', ApiShopReservations.as_view(),
         name='api_shop_reservations'),
    path('api/reserve_slot/', ApiReserveTimeSlot.as_view(),
         name='api_reserve_slot')
]
