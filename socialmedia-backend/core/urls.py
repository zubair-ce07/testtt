from rest_framework_simplejwt import views as jwt_views
from django.urls import path, re_path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

app_name = 'core'

urlpatterns = [
    path('posts/<int:pk>', views.PostView.as_view()),
    path('posts/', views.PostView.as_view()),

    path('followings/<int:pk>', views.FollowingView.as_view()),
    path('followings/', views.FollowingView.as_view()),

    path('comments/', views.CommentView.as_view()),

    path('feed/<int:user_id>', views.FeedView.as_view()),

    path('register', views.RegistrationView.as_view()),
    path('login', views.LoginView.as_view()),
    path('login/refresh', jwt_views.TokenRefreshView.as_view()),

    path('', include(router.urls)),
]
