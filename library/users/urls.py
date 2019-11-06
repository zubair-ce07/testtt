from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from users import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.UserCreateAPIView.as_view(),name='user-register'),
    path('users/', views.UserList.as_view(),name='user-list'),
    path('users/<int:pk>/', views.UserDetail.as_view(),name='user-detail'),
    path('rest-auth/', include('rest_auth.urls')),
]