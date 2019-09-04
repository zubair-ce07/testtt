"""shop url module"""
from django.urls import path

from shop import views as shop_views

urlpatterns = [
    path('profile/', shop_views.ProfileView.as_view(), name='shop_profile'),
    path('api/profile/', shop_views.ShopUpdateApiView.as_view(),
         name='api_shop_profile'),
    path('saloons/', shop_views.SaloonListView.as_view(), name='shop_list'),
    path('api/saloons/', shop_views.ShopListApiView.as_view(), name='api_shop_list'),
    path('shop/<str:shop_name>', shop_views.SaloonSlotListView.as_view(),
         name='shop_slots'),
    path('api/shop/<str:shop_name>', shop_views.ListSaloonSlotsApiView.as_view(),
         name='api_shop_slots'),
    path('api/cancel-reservation/<int:pk>', shop_views.DeleteReservationApiView.as_view(),
         name='api_delete_slots'),
    path('mysaloon/', shop_views.MyShopListView.as_view(), name='my_shop'),
    path('api/mysaloon/', shop_views.ListAddTimeSlotsApiView.as_view(),
         name='api_my_shop'),
    path('myreservations/', shop_views.ReservationsListView.as_view(),
         name='shop_reservations'),
    path('api/myreservations/', shop_views.ShopReservationsApiView.as_view(),
         name='api_shop_reservations'),
    path('api/reserve_slot/', shop_views.ReserveTimeSlotApiView.as_view(),
         name='api_reserve_slot'),
    path('api/add_review/', shop_views.AddReviewApiView.as_view(),
         name='api_add_review')
]
