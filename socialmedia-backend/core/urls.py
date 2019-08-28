from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path, re_path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
# router.register(r'posts', views.PostViewSet)
# router.register(r'comments', views.CommentViewSet)
# router.register(r'followings', FollowingViewSet)

app_name = 'core'

urlpatterns = [
    # re_path(r'posts/(?:<int:pk>)?', views.PostAPIView.as_view()),
    path('posts/<int:pk>', views.PostAPIView.as_view()),
    path('posts/', views.PostAPIView.as_view()),

    path('followings/<int:id>', views.FollowingAPIView.as_view()),
    path('followings/', views.FollowingAPIView.as_view()),

    path('comments/', views.CommentAPIView.as_view()),

    path('feed/<int:user_id>', views.FeedAPIView.as_view()),

    path('register', views.RegistrationAPIView.as_view()),
    path('login', views.LoginAPIView.as_view()),
    path('login/refresh', TokenRefreshView.as_view()),

    path('', include(router.urls)),
]
