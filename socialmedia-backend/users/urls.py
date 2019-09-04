from django.urls import path, include
from rest_framework import routers

from users import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'friends', views.FriendListViewSet)

app_name = 'users'

urlpatterns = [
    path('users/<int:pk>/posts/', views.UserPostView.as_view()),
    path('users/<int:pk>/friends/', views.UserFriendListView.as_view()),

    path('register', views.RegistrationView.as_view()),
    path('login', views.LoginView.as_view()),
    path('login/refresh', views.LoginRefreshView.as_view()),
]
