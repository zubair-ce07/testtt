from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('profile/', views.Index.as_view(), name='index'),
    path('profile/<int:pk>', views.ProfileDetails.as_view(), name='details'),
    path('profile/<int:pk>/update/',
         views.ProfileUpdate.as_view(),
         name='profile_update'),
    path('profile/signup/', views.SignUp.as_view(), name='signup'),
    path('profile/', include('django.contrib.auth.urls')),
]
