from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.HomepageView.as_view(), name='index'),
    path('upload/', views.UploadsView.as_view(), name='upload'),
    path('my_uploads/', views.MyUploadsView.as_view(), name='my_uploads'),
    path('favorites/', views.MyFavoritesView.as_view(), name='favorites'),
    path('settings/', views.MySettings.as_view(), name='settings'),
]
