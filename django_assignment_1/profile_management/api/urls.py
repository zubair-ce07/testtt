from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from profile_management.api import views

urlpatterns = [
    path('', views.list_users, name='list'),
    path('<int:pk>/', views.get_user, name='get'),
    path('<int:pk>/update', views.update_user, name='update'),
    path('<int:pk>/delete', views.delete_user, name='delete'),
    path('signup', views.create_user, name='create'),
    path('login', obtain_auth_token, name='get_user_auth_token'),
]
